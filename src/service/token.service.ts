import {Config, Inject, Provide} from "@midwayjs/core";
import {InjectEntityModel} from "@midwayjs/typeorm";
import {Repository} from "typeorm";
import {UserEntity} from "../entity/user.entity";
import {TokenEntity} from "../entity/token.entity";
import {RedisService} from "@midwayjs/redis";
import {UserService} from "./user.service";


@Provide()
export class TokenService {

  @InjectEntityModel(UserEntity)
  user: Repository<UserEntity>;
  @InjectEntityModel(TokenEntity)
  token: Repository<TokenEntity>;

  @Config('common')
  common
  @Inject()
  redis: RedisService;

  @Inject()
  userService: UserService;

  async getAccessToken(email: string, clientToken: string) {

    const userData = await this.user.findOne(
      {
        where: {email: email}
      }
    )

    if (userData.permission != 0) {

    }

    return
  }

  async searchUserByAccessToken(accessToken: string): Promise<any> {
    return new Promise(async (resolve) => {
      const tokenData = await this.token.findOne(
        {
          where: {accessToken: accessToken}
        }
      );
      const user = tokenData.user;
      if (user) {
        resolve(user);
      } else {
        resolve(false);
      }
    });
  }

  async refreshAccessToken(accessToken: string, clientToken: string): Promise<any> {
    const accessData = await this.user.find({
        relations: ["user"],
      }
    );
    return new Promise(async (resolve) => {
      for (let i = 0; i < accessData.length; i += 1) {
        const user = accessData[i];
        if (user && user.permission != 0) {
          let tokenIndex = -1;
          for (let i = 0; i < user.tokens.length; i += 1) {
            if (user.tokens[i].accessToken === accessToken) {
              tokenIndex = i;
              break;
            }
          }

          // 未找到指定accessToken
          if (tokenIndex === -1) {
            resolve(false);
            return;
          }

          // clientToken不匹配
          if (clientToken) {
            if (clientToken !== user.tokens[tokenIndex].clientToken) {
              resolve(false);
              return;
            }
          }

          // accessToken已过期
          if (Date.now() - user.tokens[tokenIndex].createAt >= 432000000) {
            await this.token.remove(user.tokens[tokenIndex]);
            await this.user.save(user);
            resolve(false);
            return;
          }

          Object.assign(user.tokens[tokenIndex], {status: 1});
          await this.user.save(user);
          resolve({
            accessToken: user.tokens[tokenIndex].accessToken,
            clientToken: user.tokens[tokenIndex].clientToken,
            uuid: user.uuid,
            playername: user.playerName
          })
          return;
        }
      }
      resolve(false);
    });

  }

  async validateAccessToken(accessToken: string, clientToken: string): Promise<any> {
    const accessData = await this.user.find({
        relations: ["user"],
      }
    );
    return new Promise(async (resolve) => {
      for (let i = 0; i < accessData.length; i += 1) {
        const user = accessData[i];
        if (user && user.permission != 0) {
          let tokenIndex = -1;
          for (let i = 0; i < user.tokens.length; i += 1) {
            if (user.tokens[i].accessToken === accessToken) {
              tokenIndex = i;
              break;
            }
          }

          // 未找到指定accessToken
          if (tokenIndex === -1) {
            resolve(false);
            return;
          }

          // clientToken不匹配
          if (clientToken) {
            if (clientToken !== user.tokens[tokenIndex].clientToken) {
              resolve(false);
              return;
            }
          }

          // accessToken已过期
          if (Date.now() - user.tokens[tokenIndex].createAt >= 432000000) {
            await this.token.remove(user.tokens[tokenIndex]);
            await this.user.save(user);
            resolve(false);
            return;
          }

          Object.assign(user.tokens[tokenIndex], {status: 1});
          await this.user.save(user);
          resolve(true);
          return;
        }
      }
      resolve(false);
    });

  }

  async invalidateAccessToken(accessToken: string): Promise<any> {
    const accessData = await this.user.find({
        relations: ["user"],
      }
    );
    return new Promise(async (resolve) => {
      for (let i = 0; i < accessData.length; i += 1) {
        const user = accessData[i];
        if (user && user.permission != 0) {
          let tokenIndex = -1;
          for (let i = 0; i < user.tokens.length; i += 1) {
            if (user.tokens[i].accessToken === accessToken) {
              tokenIndex = i;
              break;
            }
          }

          // 未找到指定accessToken
          if (tokenIndex === -1) {
            resolve(false);
            return;
          }

          await this.token.remove(user.tokens[tokenIndex]);
          await this.user.save(user);
          resolve(true);
          return;

        }
      }
      resolve(false)
    });
  }

  async invalidateAllAccessToken(email: string, password: string): Promise<any> {
    const user = await this.user.findOne({
        where: {email: email}
      }
    );
    return new Promise(async (resolve) => {
      if (user && user.permission != 0) {
        // 密码不正确
        if (password !== user.password) {
          resolve(false)
        }
        // 遍历所有token并删除
        for (let i = 0; i < user.tokens.length; i += 1) {
          await this.token.remove(user.tokens[i])
        }
        Object.assign(user, user.tokens)
        await this.user.save(user);
        resolve(true)
      } else {
        resolve(false)
      }
    });

  }

  async clientToServerValidate(accessToken, selectedProfile, serverId, ip): Promise<any> {
    return new Promise(async (resolve) => {
      this.searchUserByAccessToken(accessToken).then((result) => {
        // 无法找到accessToken
        if (!result) {
          resolve(false)
          return
        }

        // 令牌对应用户已被封禁
        if (result.isBanned) {
          resolve(false)
          return
        }

        if (!this.common.ignoreEmailVerification) {
          // 令牌对应用户未验证邮箱
          if (!result.verified) {
            resolve(false)
            return
          }
        }

        // 令牌对应玩家uuid不一致
        if (result.uuid.replace(/-/g, '') !== selectedProfile) {
          resolve(false)
          return
        }

        let data = JSON.stringify({
          accessToken,
          selectedProfile,
          username: result.playername,
          ip
        })

        // 将授权信息储存至redis，15秒过期
        this.redis.set(`serverId_${serverId}`, data, 'EX', 15).then(() => {
          resolve(true)
        })

      })

    });

  }

  async serverToClientValidate(username, serverId, ip): Promise<any> {
    return new Promise(async (resolve) => {
      // 根据serverId获取对应授权信息
      this.redis.get(`serverId_${serverId}`, (err, response) => {
        // 未找到对应授权信息或发生错误
        if (err || !response) {
          resolve(false)
          return
        }

        const clientData = JSON.parse(response)

        // 玩家名称与授权不对应
        if (clientData.username !== username) {
          resolve(false)
          return
        }

        // 若提供了客户端ip，则需要判断储存的客户端ip与其是否一致
        if (ip) {
          if (clientData.ip !== ip) {
            resolve(false)
            return
          }
        }

        // 根据accessToken获取玩家资料
        module.exports.searchUserByAccessToken(clientData.accessToken).then((result) => {
          // 生成玩家完整Profile
          const data = this.userService.genUserProfile(result)
          resolve(data)
        })
      })

    });

  }

}
