import React, { Component } from 'react';
import io from "socket.io-client";
import myImage from '../images/redChat.png'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faUsers, faUser, faUserFriends } from '@fortawesome/free-solid-svg-icons'; // Example icon group
import { faCoffee } from '@fortawesome/free-solid-svg-icons';
import { events } from 'socket.io/lib/namespace';

const socket = io('http://127.0.0.1:7000');



class chat extends Component {

  constructor() {
    super();
    socket.emit('get_names');
  
  }

  state = {
    name: "",
    message: "",
    namecollection: [],
    currentUser : "",
    chatUser : "",
    chatMessages : []
  }

  handleChange(event) {
    this.setState({ message: event.target.value });
  }

  componentDidUpdate() {
    this.scrollToBottom();
  }
  
  scrollToBottom() {
    this.messagesEnd.scrollIntoView({ behavior: "smooth" });
  }

  componentDidMount() {

    this.scrollToBottom();

    socket.on("namecollection", (users) => {
      // console.log("users",users)
      const currentUserDetail = users.find(m=> m.name === global.currentUser);
      // console.log("currentUserDetail",currentUserDetail)
      if(currentUserDetail != null)
      {
        if(this.state.currentUser.length === 0)
        {
            this.setState({ currentUser: currentUserDetail });
        }
      }
      this.setState({ namecollection: users });
    });

    socket.on("get_messages", (messages) => {
      // console.log(messages);
      this.setState({ chatMessages: messages });
    });
  }

  sendMessage(){
    let messageDetails = {
      message : this.state.message,
      userid : this.state.currentUser.name, 
      userimg : this.state.currentUser.photo
    }
    this.state.message = messageDetails.message
    this.setState({ message: "",userid:"" });
    socket.emit('send_message', messageDetails);
    
  }

  keyPress(e){
    if(e.keyCode === 13){
      e.preventDefault();
      let messageDetails = {
        message : this.state.message,
        userid : this.state.currentUser.name, 
        userimg : this.state.currentUser.photo
      }
      this.setState({ message: "",userid:"" });
      socket.emit('send_message', messageDetails);
    }
  }
  
  render() {
    return (
      <React.Fragment>
        {/* <div>
        </div> */}
        <div id="sidepanel">
        <img id="redChatLogo" src={myImage} alt="My Image" />
          <div id="profile">
            <div className="wrap">
            <img id="profile-img" src={"images/" + this.state.currentUser.photo} className="online" alt="" />
              <p>{this.state.currentUser.name}</p>
            </div>
          </div>
          <div id="search">
           &nbsp;
          </div>
          <div id="contacts">
            <ul>
              {this.state.namecollection.filter(m => m.name !== global.currentUser).map((p, i) => {
                return (
                  <li className="contact" key={i}>
                    <div className="wrap">
                      <span className="contact-status online"></span>
                      <img src={"images/" + p.photo} alt="" />
                      <div className="meta">
                        <p className="name" style={{fontSize:'20px', paddingTop:'5px'}}>{p.name}</p>
                      </div>
                    </div>
                  </li>)
              })}
            </ul>
          </div>
        </div>
        <div className="content">
          <div className="contact-profile" >
          <FontAwesomeIcon icon={faUsers}  style={{color: "#E6545B",marginLeft: "2%"}} />
          <p style={{marginLeft: "5%",  fontWeight: "bold",}}><b>Pune-Hyd Shivneri Travels</b></p>
          </div>
          <div className="messages">
            <ul>
              {
                this.state.chatMessages != null && this.state.chatMessages.map((p, i) => {
                  return(<li key={i} className={this.state.currentUser.name === p.userid ? "replies" : "sent"}>
                      <img src={"images/" + p.userimg}  alt="" />
                      <p>{p.message}</p>
                  </li>)
                })
              }
            </ul>
            <div style={{ float:"left", clear: "both" }}
                ref={(el) => { this.messagesEnd = el; }}>
            </div>
          </div>
          <div className="message-input">
            <div className="wrap">
              <input onKeyDown={this.keyPress.bind(this)} onChange={this.handleChange.bind(this)} value={this.state.message}  type="text" placeholder="Write your message..." />
              <button onClick={this.sendMessage.bind(this)} className="submit"><i className="fa fa-paper-plane" aria-hidden="true"></i></button>
            </div>
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default chat;
