import {MidwayConfig} from '@midwayjs/core';
import {IpEntity} from '../entity/ip.entity';
import {SkinEntity} from '../entity/skin.entity';
import {TokenEntity} from '../entity/token.entity';
import {UserEntity} from '../entity/user.entity';
import path = require('path');

export default {
  // use for cookie sign key, should change to your own and keep security
  keys: '1679482516514_8737',
  koa: {
    port: 7001,
  },
  typeorm: {
    dataSource: {
      default: {
        type: 'sqlite',
        database: path.join(__dirname, '../../test.sqlite'),
        synchronize: false,
        logging: false,
        entities: [UserEntity, SkinEntity, IpEntity, TokenEntity],
      },
    },
  },
  common: {
    //站点名称
    sitename: 'MineSkin',
    //站点描述
    description: '轻量的MC服务器yggdrasil验证',
    //是否忽略用户邮箱验证
    ignoreEmailVerification: false,
    //站点链接，主要用于Yggdrasil认证（末尾不加/）
    url: 'http://example.com',
    //页脚相关设置
    footer: {
      copyright: 'Powered By cnlimiter.',
      //页脚链接
      links: [
        {
          title: 'MineSkin',
          link: "https://skin.evolvefield.cn",
          target: '_self'
        },
        {
          title: 'Github',
          link: "https://github.com/cnlimiterm/MineSkin",
          target: '_blank'
        }
      ]
    },
  },
  extra: {
    //资源可信域列表，删除样例域名，然后将你网站的域名加入到下面列表中
    //游戏会拒绝非可信域的材质加载
    //加句点.能够使用泛域(如.example2.com)
    skinDomains: [],
    signature: {
      private: '|-\n' +
        '      -----BEGIN RSA PRIVATE KEY-----\n' +
        '      私钥\n' +
        '-----END RSA PRIVATE KEY-----',
      public: '|-\n' +
        '  -----BEGIN PUBLIC KEY-----\n' +
        '  公钥\n' +
        '-----END PUBLIC KEY-----'
    }
  }
} as MidwayConfig;
