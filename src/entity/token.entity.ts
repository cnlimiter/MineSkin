import {Column, Entity, PrimaryGeneratedColumn, UpdateDateColumn,} from 'typeorm';

@Entity()
export class TokenEntity {
  @PrimaryGeneratedColumn()
  id: number;

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
