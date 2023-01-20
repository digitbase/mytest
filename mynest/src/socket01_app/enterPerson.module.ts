import { Module } from '@nestjs/common';
import { pr } from '../comm/fun.comm';
import { OnModuleInit } from '@nestjs/common';
import {
  WebSocketGateway,
  SubscribeMessage,
  MessageBody,
  WebSocketServer,
} from '@nestjs/websockets';
import { Server } from 'socket.io';

@WebSocketGateway(3001,{ namespace: 'dahua_002' })
export class EnterPersonModule implements OnModuleInit {
  @WebSocketServer()
  server: Server;

  onModuleInit(): void {
    this.server.on('connection', (socket) => {
      pr(socket.id, 8800);
    });
  }


  @SubscribeMessage('sendMsg')
  async pushMsg(@MessageBody() createDDto) {
    pr(createDDto)
    let body = JSON.parse(createDDto);

    let topic = body['topic'] ? body['topic'] : "test";
    let msg = body['msg'] ? body['msg'] : "this is msg";
    let res = this.dahuaSendMsg(topic, msg);

  }


  @WebSocketServer()
  dahuaSendMsg(topic: string, message: any) {
    pr(`topic:${topic} msg:${message}`, 7733)
    
    let res = this.server.emit(topic, message)
    return res;
  }
}
