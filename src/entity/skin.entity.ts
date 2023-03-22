import {Column, Entity, PrimaryGeneratedColumn} from 'typeorm';

@Entity()
export class SkinEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({
    default: 0,
  })
  type: number;

  @Column({
    default: '9b155b4668427669ca9ed3828024531bc52fca1dcf8fbde8ccac3d9d9b53e3cf',
  })
  hash: string;
}
