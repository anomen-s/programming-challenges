import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-servers',
  templateUrl: './servers.component.html',
  styleUrls: ['./servers.component.css']
})
export class ServersComponent implements OnInit {

  allowNewServer = false;
  serverCreationStatus = 'nothing';
  serverName = '';
  
  constructor() {
     setTimeout(() => {
       this.allowNewServer = true;
     }, 2000);
  }

  ngOnInit(): void {
  
  }
  
  onCreateServer(event: any) {
     this.serverCreationStatus = 'Server '+this.serverName+' created';
     console.log(event);
  }

  onUpdateServerName(event: any) {
     const name = (<HTMLInputElement>event.target).value;
     console.log('Server name: ' + name);
     this.allowNewServer = (name != '');
  }

}
