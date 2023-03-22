import {Provide} from '@midwayjs/core';
import {InjectEntityModel} from '@midwayjs/typeorm';
import {Repository} from 'typeorm';
import {IUserOptions} from '../interface';
import {UserEntity} from "../entity/user.entity";

@Provide()
export class UserService {
  @InjectEntityModel(UserEntity)//注入数据库
  user: Repository<UserEntity>;


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
}
