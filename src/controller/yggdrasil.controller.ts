import {Body, Config, ContentType, Controller, Get, Inject, Post, Query} from '@midwayjs/core';
import {Context} from '@midwayjs/koa';
import {UserService} from '../service/user.service';
import {Response} from "../util/response";
import {TokenService} from "../service/token.service";

const pkg = require('../../package.json');

@Controller('/api/yggdrasil')
export class YggdrasilController {

  //注入上下文
  @Inject()
  ctx: Context;
  //注入操作
  @Inject()
  userService: UserService;

  @Inject()
  tokenService: TokenService;
  //注入配置
  @Config('common')
  common;
  @Config('extra')
  extra;

  async getUser(@Query('uid') uid) {
    const user = await this.userService.getUser({uid});
    return {success: true, message: 'OK', data: user};
  }

  @Get('/')// Yggdrasil信息获取接口
  @ContentType('application/json')
  async yggdrasil() {
    return {
      meta: {
        implementationName: `${this.common.sitename}(MineSkin Yggdrasil)`, // Yggdrasil协议名称
        implementationVersion: pkg.version, // Yggdrasil协议版本
        serverName: this.common.sitename, // Yggdrasil认证站点名称
        links: {
          homepage: this.common.url,
          register: `${this.common.url}/register`
        }
      },
      skinDomains: this.extra.skinDomains, // 可信域（皮肤加载所信任的域名）
      signaturePublicKey: this.extra.signature.public // 签名公钥
    };
  }

  @Post('/api/profiles/minecraft')
  async getProfiles(@Body() body) {

  }

  @Post('/authserver/refresh')
  async refresh(@Body() data) {
    if (!data.accessToken) {
      Response(this.ctx).invalidToken();
      return;
    }

    const {accessToken} = data;
    const {clientToken} = data;
    const requestUser = data.requestUser || false;

    // 刷新令牌
    const result = await this.tokenService.refreshAccessToken(accessToken, clientToken).then((ret) => ret);

    // 刷新操作失败
    if (!result) {
      Response(this.ctx).invalidToken();
      return;
    }

    const profileData = {
      id: result.uuid.replace(/-/g, ''),
      name: result.playername
    }

    const responseData = {
      accessToken: result.accessToken,
      clientToken: result.clientToken,
      selectedProfile: profileData,
      user: {}
    }
    if (requestUser) {
      responseData.user = {
        id: result.uuid.replace(/-/g, '')
      }
    }
    Response(this.ctx).success(responseData);
  }


}
