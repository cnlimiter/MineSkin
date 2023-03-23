import {Column, Entity, ManyToOne, PrimaryGeneratedColumn, UpdateDateColumn,} from 'typeorm';
import {UserEntity} from "./user.entity";

@Entity()
export class TokenEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @ManyToOne(type => UserEntity, user => user.tokens)
  user: UserEntity;

  @Column()
  accessToken: string;

  @Column()
  clientToken: string;

  @Column({
    default: 1,
  })
  status: number;

  @UpdateDateColumn()
  createAt: number;
}
