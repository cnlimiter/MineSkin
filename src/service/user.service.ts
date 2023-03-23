import {Config, Provide} from '@midwayjs/core';
import {InjectEntityModel} from '@midwayjs/typeorm';
import {Repository} from 'typeorm';
import {IUserOptions} from '../interface';
import {UserEntity} from "../entity/user.entity";
import * as crypto from "crypto";


@Provide()
export class UserService {
  @InjectEntityModel(UserEntity)//注入数据库
  user: Repository<UserEntity>;

  @Config('common')
  common

  @Config('extra')
  extra

  async getUser(options: IUserOptions) {
    return {
      uid: options.uid,
      username: 'mockedName',
      phone: '12345678901',
      email: 'xxx.xxx@xxx.com',
    };
  }

  async searchUserInfoByPlayerName(playername: string) {
    return await this.user.findOne({
      where: {playerName: playername}
    });
  }

  async genUserProfile(userData, isPropertiesContained = true) {
    let data
    let textureData
    if (isPropertiesContained) {
      textureData = {
        timestamp: Date.now(),
        profileId: userData.uuid.replace(/-/g, ''),
        profileName: userData.playername,
        textures: {
          SKIN: {
            url: `${this.common.url}/textures/${userData.skin.hash}`,
            metadata: {
              model: userData.skin.type === 0 ? 'default' : 'slim'
            }
          }
        }
      }
      textureData = Buffer.from(JSON.stringify(textureData)).toString('base64')
    }
    if (isPropertiesContained) {
      data = {
        id: userData.uuid.replace(/-/g, ''),
        name: userData.playername,
        properties: [
          {
            name: 'textures',
            value: textureData,
            signature: this.genSignedData(textureData)
          }
        ]
      }
    } else {
      data = {
        id: userData.uuid.replace(/-/g, ''),
        name: userData.playername
      }
    }

    return data
  }

  genSignedData(data): string {
    const sign = crypto.createSign('SHA1')
    sign.update(data)
    sign.end()
    const signature = sign.sign(this.extra.signature.private)
    return signature.toString('base64')
  }
}
