import {Column, Entity, PrimaryGeneratedColumn} from 'typeorm';

@Entity()
export class IpEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  register: string;

  @Column()
  lastLogged: string;
}
