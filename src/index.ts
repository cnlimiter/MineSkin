import {AppDataSource} from "./data-source"
import {User} from "./entity/User"
import {Ip} from "./entity/Ip";
import {Token} from "./entity/Token";
import {Skin} from "./entity/Skin";

AppDataSource.initialize().then(async () => {

    console.log("Inserting a new user into the database...")
    const user = new User()
    const ip = new Ip()
    const token = new Token()
    const skin = new Skin()
    user.uuid = "xxxxxx"
    user.playerName = "Player"
    user.password = "test"
    user.email = "123456@qq.com"

    token.clientToken = ""
    token.accessToken = ""

    ip.register = ""
    ip.lastLogged = ""

    user.ip = ip
    user.token = token
    user.skin = skin

    await AppDataSource.manager.save(ip)
    await AppDataSource.manager.save(token)
    await AppDataSource.manager.save(skin)
    await AppDataSource.manager.save(user)
    console.log("Saved a new user with id: " + user.id)

    console.log("Loading users from the database...")
    const users = await AppDataSource.manager.find(User)
    console.log("Loaded users: ", users)

    console.log("Here you can setup and run express / fastify / any other framework.")

}).catch(error => console.log(error))
