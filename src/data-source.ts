import "reflect-metadata"
import {DataSource} from "typeorm"
import {User} from "./entity/User"
import {Skin} from "./entity/Skin";
import {Ip} from "./entity/Ip";
import {Token} from "./entity/Token";

export const AppDataSource = new DataSource({
    type: "sqlite",
    database: "database.sqlite",
    synchronize: true,
    logging: false,
    entities: [User, Skin, Ip, Token],
    migrations: [],
    subscribers: [],
})
