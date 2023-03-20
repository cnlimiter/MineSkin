import {Column, Entity, PrimaryGeneratedColumn} from "typeorm"


@Entity()
export class Ip {
    @PrimaryGeneratedColumn()
    id: number

    @Column()
    register: string

    @Column()
    lastLogged: string
}


