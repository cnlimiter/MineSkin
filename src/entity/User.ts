import {Column, CreateDateColumn, Entity, JoinColumn, OneToOne, PrimaryGeneratedColumn, UpdateDateColumn} from "typeorm"
import {Ip} from "./Ip";
import {Skin} from "./Skin";
import {Token} from "./Token";

@Entity()
export class User {

    @PrimaryGeneratedColumn()
    id: number

    @Column()
    uuid: string

    @Column()
    playerName: string

    @Column()
    password: string

    @Column()
    email: string

    @Column({
        default: false
    })
    verified: boolean

    @Column({
        default: false
    })
    isBanned: boolean

    @OneToOne(() => Skin)
    @JoinColumn()
    skin: Skin

    @OneToOne(() => Token)
    @JoinColumn()
    token: Token

    @OneToOne(() => Ip)
    @JoinColumn()
    ip: Ip

    @CreateDateColumn()
    register: number

    @UpdateDateColumn()
    lastLogged: number
}
