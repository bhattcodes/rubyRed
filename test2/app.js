const express = require('express')
const app = express()
const server = require('http').createServer(app);
const io = require('socket.io')(server);
const http = require('http');

var  jsonObject=[]
var  messagesFromServer=[]

var dataObjFromDB ={}


var nameCollection = [];
var messageCollection = [];
const cors = require('cors'); //added new

const corsOptions = {
  origin: 'http://localhost:3000',
  credentials: true, // Allow credentials (cookies, HTTP authentication, etc.)
};

app.use(cors(corsOptions));

var i = 0;
//var travellers = [{"userid": 242335,"timeStamp": 388484838,"message":"NEWUSER"}];
// var OnlineUsers = [{"id": 1,"name": "Louis Litt","photo": "louislitt.png","status": "online","lastmessage": "You just got LITT up, Mike."},{"id": 2,"name": "Harvey Specter","photo": "harveyspecter.png","status": "online","lastmessage": "Wrong. You take the gun, or you"},{"id": 3,"name": "Rachel Zane","photo": "rachelzane.png","status": "online","lastmessage": "I was thinking that we could have."},{"id": 4,"name": "Donna Paulsen","photo": "donnapaulsen.png","status": "online","lastmessage": "Mike, I know everything! I'm Donna.."},{"id": 5,"name": "Mike Ross","photo": "mikeross.png","status": "online","lastmessage": "Rachel, I know everything! I'm Donna.."}];

var port = process.env.PORT || 7000;

app.use(express.static(__dirname + '/'));

io.on('connection', client => {

  // get collection of names
  client.on('get_names', () => {
    
      const options = {
        hostname: '127.0.0.1',
        port: 5000,
        path: '/read_messages',
        method: 'GET',
      };
    const req = http.request(options, (res) => {
      let data = '';
    
      res.on('data', (chunk) => {
        // console.log("chunk",chunk)
        data += chunk;
      });
    
      res.on('end', () => {
        // console.log(typeof data)
        // console.log(data);
        try {
          for (const key in JSON.parse(data)) {
            if (JSON.parse(data).hasOwnProperty(key)) {
              const value = JSON.parse(data)[key].message;
              console.log(`${key}: ${value}`);
              messagesFromServer = messagesFromServer.concat({"userid":JSON.parse(data)[key].userid,"message":JSON.parse(data)[key].message})
            }
          }

          // console.log("messagesFromServer",messagesFromServer);
          // console.log("messagesFromServer",typeof messagesFromServer);

        } catch (error) {
          console.error('Error parsing JSON:', error);
        }
      });
    });
    
    req.on('error', (error) => {
      console.error(`Error: ${error.message}`);
    });
    
    req.end();
    // messageCollection = messageCollection.concat(messagesFromServer);
  
    io.sockets.emit('namecollection', messagesFromServer)
  })

  client.on('send_message', (messageDetails) => {
    // console.log("messageDetails xxxxx",messageDetails)

    const postData = JSON.stringify({ "userid": messageDetails.userid,"message":messageDetails.message });

const options = {
  hostname: '127.0.0.1',  // Replace with the target hostname
  port: 5000,                // Replace with the target port (e.g., 80 for HTTP, 443 for HTTPS)
  path: '/add_message',    // Replace with the specific path you want to POST to
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': postData.length,
  },
};

const req = http.request(options, (res) => {
  let data = '';

  res.on('data', (chunk) => {
    data += chunk;
  });

  res.on('end', () => {
    console.log("ddddd",data);
    if(1){
      const options = {
        hostname: '127.0.0.1',
        port: 5000,
        path: '/read_messages',
        method: 'GET',
      };
    const req = http.request(options, (res) => {
      let data = '';
    
      res.on('data', (chunk) => {
        // console.log("chunk",chunk)
        data += chunk;
      });
    
      res.on('end', () => {
        // console.log(typeof data)
        // console.log(data);
        try {
          for (const key in JSON.parse(data)) {
            if (JSON.parse(data).hasOwnProperty(key)) {
              let newItem = [{"userid":JSON.parse(data)[key].userid,"message":JSON.parse(data)[key].message}]
              messagesFromServer = messagesFromServer.concat(newItem)
            }
          }
          io.sockets.emit('get_messages', messagesFromServer)


        } catch (error) {
          console.error('Error parsing JSON:', error);
        }
      });
    });
    
    req.on('error', (error) => {
      console.error(`Error: ${error.message}`);
    });
    
    req.end();
    
  }
  });
});

req.on('error', (error) => {
  console.error(`Error: ${error.message}`);
});

req.write(postData);
req.end();

   

  // messageCollection = messageCollection.concat(messagesFromServer);
  // messageCollection.concat({ "userid": messageDetails.userid,"message":messageDetails.message })
    
    // io.sockets.emit('get_messages', messageCollection)
  })
  client.on('add_name', (name) => {
    // console.log("name",name)
    i = i + 1;
    //test start
    
    const options = {
      hostname: '127.0.0.1',
      port: 5000,
      path: '/get_all_users',
      method: 'GET',
    };
   
    
    const req = http.request(options, (res) => {
      let data = '';
    
      res.on('data', (chunk) => {
        // console.log("chunk",chunk)
        data += chunk;
      });
    
      res.on('end', () => {
        // console.log(typeof data)
        // console.log(data);
        try {
          jsonObject=jsonObject.concat(JSON.parse(data));
          for (let i = 0; i < jsonObject.length; i++) {
            // console.log("jsonObject",jsonObject[i]);
            nameCollection[i]={"name":jsonObject[i]}
          }         
          io.sockets.emit('namecollection', nameCollection);
        } catch (error) {
          console.error('Error parsing JSON:', error);
        }
      });
    });
    
    req.on('error', (error) => {
      console.error(`Error: ${error.message}`);
    });
    
    req.end();
  
    
  })

  client.on('disconnect', () => { });
});

server.listen(port, function(){
  console.log('listening on *:7000');
});


