<!DOCTYPE html>
<head>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=PT+Sans:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
  <script src="amazon-cognito-identity.min.js"></script>
  <style>
    body {
      font-family: 'PT Sans', sans-serif;
      margin: 0;
      display: grid;
      grid-template-rows: 14% 5% 73% 9%;
      height: 100vh;
    }
    h1, h2, h3, h4, p, section {
      text-align: center;
    }
    #page-title {
      color: rgb(210,200,200);
      background-color: rgb(70,70,80);
      margin: 0;
      grid-row: 1;
    }
    #page-title h1 {
      font-size: 2.4em;
      margin: 0;
    }
    #page-title h2 {
      font-size: 1.5em;
      margin: 0;
    }

    #section-container {
      grid-row: 3;
      height: 80%;
      width: 100%;
      display: grid;
      grid-template-columns: 20% 60% 20%;
    }
    .single-section {
      grid-row: 1;
      grid-column: 2;
      display: grid;
      grid-template-columns: 7% 23% 70%;
    }
    .section-label {
      grid-column: 1/3;
      margin: 2vh 2vw 2vh 2vw;
      text-align: right;
      height: 3vh;
    }
    .section-input {
      grid-column: 3;
      margin: 2vh 4vw 2vh 4vw;
      height: 3vh;
    }
    .section-submit {
      grid-column: 1 / 4;
      margin: 2vh 16vw 2vh 16vw;
      height: 3vh;
    }
    .section-text {
      grid-column: 1 / 4;
      margin: 2vh 4vw 2vh 4vw;
      height: 3vh;
    }
    .section-tick-box {
      grid-column: 1;
      margin: 2vh 1vw 2vh 1vw;
      height: 3vh;
    }
    .section-mini-label {
      grid-column: 2;
      margin: 2vh 1vw 2vh 1vw;
      height: 3vh;
    }

    #top-menu {
      text-align: center;
      background-color: rgb(70,70,80);
      grid-row: 2;
      display: flex;
      flex-direction: column;
      justify-content: end;
    }
    .top-menu-item {
      border-width: 0.15vw 0.15vw 0.15vw 0.15vw;
      border-radius: 0.9vw 0.9vw 0 0;
      border-style: solid;
      border-color: rgb(70,70,80);
      padding: 0.2vh 1vw 0.2vh 1vw;
      font-size: 1.2em;
      background-color: white;
      color: rgb(120,120,120);
      filter: blur(0.6px);
    }
    .top-menu-item.selected {
      font-weight: bold;
      border-bottom-color: white;
      color: black;
      filter: blur(0px);
    }
    .top-menu-item.available {
      color: rgb(70,70,70);
      filter: blur(0px);
    }
    #user-data-records {
      visibility: hidden;
      width: 100%;
      grid-column: 1/4;
      display: grid;
      grid-template-columns: 30% 70%;
      border-color: rgb(30,30,30);
      border-width: 0.15vw;
      border-radius: 0.4vw;
      border-style: solid;
    }
    #user-data-records .time {
      grid-column: 1;
    }
    #user-data-records .doc {
      grid-column: 2;
    }
    #user-status {
      grid-row: 4;
      background-color: rgb(140,140,140);
      margin: 0;
      padding-top: 3vh;
    }
  </style>
</head>
<html>
  <body>
    <div id="page-title">
      <h1>Acme App Demo</h1>
      <h2>Sign In, Password Challenge, Exercise API<h2>
    </div>
    <div id="top-menu">
      <div id="top-menu-inner">
        <button id="login-item" class="top-menu-item selected">login</button>
        <button id="logout-item" class="top-menu-item">logout</button>
        <button id="send-data-item" class="top-menu-item available">send data</button>
        <button id="get-data-item" class="top-menu-item">get data</button>
      </div>
    </div>

    <div id="section-container" >
      <section id="login-form" class="single-section">
        <h2 class="section-text">login with password or temporary password</h2>
        <p id="login-info" class="section-text">(Temporary password normally sent by email!)</p>
        <label for="user-name-input" class="section-label">username:</label>
        <input id="user-name-input" class="section-input" value="{{username}}"/>
        <br/>
        <label for="password-input" class="section-label">password:</label>
        <input id="password-input" class="section-input" value="{{password}}"/>
        <br/>
        <button id="login-button" class="section-submit">log in</button>
      </section>

      <section id="new-password"  class="single-section" style="visibility:hidden;">
        <h2 class="section-text">please enter a new password</h2>
        <p class="section-text">(Client side validation not included!)</p>
        <label for="new-password-input" class="section-label">password:</label>
        <input id="new-password-input" class="section-input" value="Password8*"/>
        <br/>
        <button id="new-password-button" class="section-submit">change password</button>
      </section>

      <section id="send-user-data" class="single-section" style="visibility:hidden;">
        <label for="user-data-type-selector" class="section-label">type:</label>
        <select name="user-data-type" id="user-data-type-selector"  class="section-input">
          <option value="LOG">log</option>
          <option value="ERROR">error</option>
          <option value="RECORD">acheivement record</option>
          <option value="SUBSCRIPTION">subscription</option>
        </select>
        <br/>
        <label for="user-data-msg-input" class="section-label">content:</label>
        <input id="user-data-msg-input" class="section-input" value=""/>
        <br/>
        <button id="send-user-data-button" class="section-submit">send data</button>
        <p id="call-status" class="section-text">no record sent yet</p>
        <p class="section-text">note: subscription records cannot be sent by the user client - the option is there to try out the api failure mode.</p>
      </section>

      <section id="get-user-data" class="single-section" style="visibility:hidden;">
        <input type="checkbox" id="from-time-checkbox" class="section-tick-box" name="from-time-checkbox" value="include-from-time"/>
        <label for="from-time-checkbox" class="section-mini-label">from time</label>
        <input id="from-time-value" class="section-input" value=""/>

        <input type="checkbox" id="to-time-checkbox" class="section-tick-box" name="to-time-checkbox" value="include-to-time"/>
        <label for="to-time-checkbox" class="section-mini-label">to time</label>
        <input id="to-time-value" class="section-input" value=""/>
        <label for="get-user-data-type-selector" class="section-mini-label">record type</label>
        <select name="get-user-data-type" id="get-user-data-type-selector" class="section-input" >
          <option value="LOG">log</option>
          <option value="ERROR">error</option>
          <option value="RECORD">acheivement record</option>
          <option value="SUBSCRIPTION">subscription</option>
        </select>
        <button id="get-user-data-button" class="section-submit">get data</button>
        <p id="get-data-call-status" class="section-text">
          Default to-time is the epoch seconds time for nowish, default from-time is an hour before that.
        </p>
        <div id="user-data-records"></div>
      </section>

      <section id="logout-form" class="single-section" style="visibility:hidden;">
        <p class="section-text">
          This action will revoke and clear local token making it impossible to call any methods in
          the API gateway protected by the user's access token.  Notice it is also possible to perform
          a globalSignOut() which will revoke all the user's tokens for the application on all devices -
          if that is required.
        </p>
        <button id="logout-button" class="section-submit">logout</button>
        <p class="section-text" id="logout-status"></p>

      </section>
    </div>
    <h4 id="user-status">not logged in</h4>

    <script>
      var userPoolInstance = null;
      var cognitoUser = null;

      class Section {
        constructor(sectionId, sectionManager, cognitoClient, userStatusLine) {
          this.sectionId = sectionId;
          this.sectionManager = sectionManager;
          this.sectionManager.addSection(sectionId, this);
          this.cognitoClient = cognitoClient;
          this.userStatusLine = userStatusLine;
        }
        show() {
          this.sectionManager.hideAll();
          document.getElementById(this.sectionId).style.visibility = "visible";
        }
        hide() {
          document.getElementById(this.sectionId).style.visibility = "hidden";
        }
        showSessionError(error) {
          console.log(error);
          this.sectionManager.showOnly('login-form');
          this.cognitoClient.showLoggedIn(false);
          this.userStatusLine.set("You've been logged out with an unexpected session error.");
        }
      }

      class SectionManager {
        constructor(topMenu) {
          this.topMenu = topMenu;
          this.sectionMap = {};
          this.sectionNameToMenuItem = {
            'login-form': 'login',
            'new-password': 'login',
            'send-user-data': 'send-data',
            'get-user-data': 'get-data',
            'logout-form': 'logout'
          };
        }
        addSection(name, section) {
          this.sectionMap[name] = section;
        }
        hideAll() {
          for (var name in this.sectionMap) {
            this.sectionMap[name].hide();
          }
        }
        showOnly(sectionId) {
          this.hideAll();
          this.sectionMap[sectionId].show();
          this.topMenu.show(this.sectionNameToMenuItem[sectionId]);
        }
      }

      class LoginSection extends Section {
        constructor(sectionManager, cognitoClient, userStatusLine) {
          super('login-form', sectionManager, cognitoClient, userStatusLine);
          document.getElementById('login-button').addEventListener('click', () => this.login());
        }

        login() {
          this.cognitoClient.login(
            document.getElementById('user-name-input').value,
            document.getElementById('password-input').value,
            () => {
              this.cognitoClient.showLoggedIn(false);
            },
            () => {
              this.userStatusLine.set('new password required to complete login');
              this.sectionManager.showOnly('new-password');
            },
            () => {
              this.cognitoClient.showLoggedIn(true);
              this.sectionManager.showOnly('send-user-data');
            },
            () => {
              this.cognitoClient.showLoggedIn(true);
              this.sectionManager.showOnly('send-user-data');
            }
          )
        }
      }

      class NewPasswordSection extends Section {
        constructor(sectionManager, cognitoClient, userStatusLine) {
          super('new-password', sectionManager, cognitoClient, userStatusLine);
          document.getElementById('new-password-button').addEventListener('click', () => this.newPassword());
        }

        newPassword() {
          const newPassword = document.getElementById('new-password-input').value;
          this.cognitoClient.completePasswordChallenge(newPassword,
            () => {
              this.cognitoClient.showLoggedIn(false)
              this.userStatusLine.set('new password was not accepted')
              this.sectionManager.showOnly('login-form')
            },
            () => {
              this.cognitoClient.showLoggedIn(true)
              this.sectionManager.showOnly('send-user-data')
            },
          );
        }
      }

      class SendUserDataSection extends Section {
        constructor(sectionManager, cognitoClient, userStatusLine) {
          super('send-user-data', sectionManager, cognitoClient, userStatusLine)
          document.getElementById('send-user-data-button').addEventListener('click', () => this.sendUserData());
        }
        async sendUserData() {
          this.showCallStatus('sending user data')
          try {
            const session = await this.cognitoClient.getUserSession()
            await this.sendUserDataFromForm(session)
          } catch (error) {
            this.showSessionError(error)
          }
        }

        async sendUserDataFromForm(session) {
          const userDataType = document.getElementById('user-data-type-selector').value;
          const content = document.getElementById('user-data-msg-input').value;
          const epochSeconds = Math.floor((new Date().getTime()) / 1000);
          const payload = `{ "type": "${userDataType}", "time": ${epochSeconds}, "doc": { "content": "${content}" } }`;
          const request = new Request('{{api_url}}', {
            method: 'POST',
            body: payload,
            headers: new Headers({
              'Content-Type': 'application/json',
              'Authorization': session.getAccessToken().jwtToken,
              'Accept': 'application/json',
              'Accept-Encoding': 'gzip, deflate, br',
              'Connection': 'keep-alive'
            })
          });
          const res = await fetch(request);
          const resJSON = await res.json();
          if (res.ok) {
            this.showCallStatus("last event result: " + JSON.stringify(resJSON.body));
            document.getElementById('user-data-msg-input').value = ''
          } else {
            this.showCallStatus("caught: " + resJSON.errorMessage);
          }
        }
        showCallStatus(msg) {
          document.getElementById('call-status').innerHTML = msg;
        }
      }
      class GetUserDataSection extends Section {
        constructor(sectionManager, cognitoClient, userStatusLine) {
          super('get-user-data', sectionManager, cognitoClient, userStatusLine);
          document.getElementById('get-user-data-button').addEventListener('click', () => this.getUserData());
        }
        async getUserData() {
          this.clearRecords();
          try {
            const session = await this.cognitoClient.getUserSession();
            document.getElementById('user-data-records').innerHTML = '';
            await this.getUserDataFromForm(session);
          } catch (error) {
            this.showSessionError(error);
          }
        }
        async getUserDataFromForm(session) {
          const useFromTime = document.getElementById('from-time-checkbox').checked;
          const fromTime = document.getElementById('from-time-value').value;
          const useToTime = document.getElementById('to-time-checkbox').checked;
          const toTime = document.getElementById('to-time-value').value;
          const dataType = document.getElementById('get-user-data-type-selector').value;

          var apiUrl = `{{api_url}}?type=${dataType}`;
          if (useFromTime ) {
            apiUrl += `&from=${fromTime}`;
          }

          if (useToTime) {
            apiUrl += `&to=${toTime}`;
          }
          const request = new Request(apiUrl, {
            method: 'GET',
            headers: new Headers({
              'Content-Type': 'application/json',
              'Authorization': session.getAccessToken().jwtToken,
              'Accept': 'application/json',
              'Accept-Encoding': 'gzip, deflate, br',
              'Connection': 'keep-alive'
            })
          });
          const res = await fetch(request);
          const resJSON = await res.json();

          if (res.ok) {
            this.showCallStatus("last event result contained " + resJSON.body.length + " records");
            document.getElementById('user-data-records').style.visibility = 'visible';
            this.showRecords(resJSON);
          } else {
            this.showCallStatus("caught: " + resJSON.errorMessage);
          }
        }
        showRecords(resJSON) {
          var markup = '';
          for (var index in resJSON.body) {
            const record = resJSON.body[index];
            console.log("record = " + record)
            markup += `<span class="time">${record["EpochTime"]}</span><span class="doc">${JSON.stringify(record["Doc"])}</span>`;
          }
          document.getElementById('user-data-records').innerHTML = markup;
          document.getElementById('user-data-records').style.visibility = 'visible';
        }
        clearRecords() {
          document.getElementById('user-data-records').innerHTML = '';
          document.getElementById('user-data-records').style.visibility = 'hidden';
        }
        showCallStatus(msg) {
          document.getElementById('get-data-call-status').innerHTML = msg;
        }
        show() {
          const epochSeconds = Math.floor((new Date().getTime()) / 1000);
          document.getElementById('from-time-value').value = epochSeconds - 3600;
          document.getElementById('to-time-value').value = epochSeconds;
          document.getElementById('get-data-call-status').innerHTML =
            'Default to-time is the epoch seconds time for nowish, default from-time is an hour before that.';
          super.show()
        }
        hide() {
          this.clearRecords()
          super.hide()
        }
      }
      class LogoutSection extends Section {
        constructor(sectionManager, cognitoClient, userStatusLine) {
          super('logout-form', sectionManager, cognitoClient, userStatusLine)
          document.getElementById('logout-button').addEventListener('click', () => this.logout());

        }
        logout() {
          var x = this.cognitoClient.logout(() => this.logoutCallback);
          this.cognitoClient.showLoggedIn(false);
          this.sectionManager.showOnly('login-form');
        }
        logoutErrorCallback(err) {
          this.userStatusLine.set("logout failed : " + err );
          this.sectionManager.showOnly('logout-form');
        }
      }
      class UserStatusLine {
        constructor() {
          this.element = document.getElementById('user-status')
        }
        set(lineMessage) {
          this.element.innerHTML = lineMessage
        }
      }

      class TopMenu {
        constructor() {
          this.items = {
            "login" : document.getElementById("login-item"),
            "logout" : document.getElementById("logout-item"),
            "send-data" : document.getElementById("send-data-item"),
            "get-data" : document.getElementById("get-data-item")
          }
        }
        show(itemName) {
          for(var name in this.items) {
            this.items[name].classList.remove('selected');
            this.items[name].classList.remove('available');
          }
          if(itemName == 'login'){
            this.items['login'].classList.add('selected');
          } else if (itemName == 'logout'){
            this.items['logout'].classList.add('selected');
            this.items['send-data'].classList.add('available')
            this.items['get-data'].classList.add('available')
          } else if (itemName == 'send-data'){
            this.items['send-data'].classList.add('selected');
            this.items['logout'].classList.add('available')
            this.items['get-data'].classList.add('available')
          } else if (itemName == 'get-data') {
            this.items['get-data'].classList.add('selected');
            this.items['logout'].classList.add('available')
            this.items['send-data'].classList.add('available')
          }

        }
      }

      class CognitoClient {
        constructor(userStatusLine) {
          const poolData = {
            UserPoolId: '{{userpool_id}}',
            ClientId: '{{userpool_client_id}}'
          }
          this.userPoolInstance = new AmazonCognitoIdentity.CognitoUserPool(poolData);
          this.userStatusLine = userStatusLine
        }
        getUserPool() {
          return this.userPoolInstance;
        }
        login(username, password, failureCallback, newPasswordRequiredCallback, successCallback, authSuccessCallback) {
          const authenticationFlowType='USER_PASSWORD_AUTH'
          const userData = { Username: username, Pool: this.getUserPool() }
          this.cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
          this.cognitoUser.setAuthenticationFlowType(authenticationFlowType)
          const deets = new AmazonCognitoIdentity.AuthenticationDetails({ Username: username, Password: password })
          const callbackMap = {
            onFailure: failureCallback,
            newPasswordRequired: newPasswordRequiredCallback,
            onSuccess: successCallback,
            authSuccess: authSuccessCallback
          }
          this.cognitoUser.authenticateUser(deets, callbackMap)
        }
        completePasswordChallenge(newPassword, failureCallback, successCallback) {
          const callbackMap = {
            onFailure: failureCallback,
            onSuccess: successCallback
          }
          this.cognitoUser.completeNewPasswordChallenge(newPassword, {}, callbackMap, {})
        }
        logout(callback) {
          this.cognitoUser.signOut(callback)
        }
        async getUserSession() {
          return new Promise((resolve, reject) => {
            this.cognitoUser.getSession((error, session) => {
              if(error != null) {
                reject(error)
              } else {
                resolve(session)
              }
            })
          })
        }
        showLoggedIn(isLoggedIn) {
          if (isLoggedIn) {
            this.userStatusLine.set('logged in as: ' + this.cognitoUser.getUsername());
          } else {
            this.userStatusLine.set('not logged in');
          }
        }
      }

      class App {
        constructor() {
          const userStatusLine = new UserStatusLine()
          const topMenu = new TopMenu()
          this.sectionManager =  new SectionManager(topMenu)
          const cognitoClient = new CognitoClient(userStatusLine)
          this.loginSection = new LoginSection(this.sectionManager, cognitoClient, userStatusLine)
          this.newPasswordSection = new NewPasswordSection(this.sectionManager, cognitoClient, userStatusLine)
          this.sendUserDataSection = new SendUserDataSection(this.sectionManager, cognitoClient, userStatusLine)
          this.getUserSection = new GetUserDataSection(this.sectionManager, cognitoClient, userStatusLine)
          this.logoutSection = new LogoutSection(this.sectionManager, cognitoClient, userStatusLine)

          document.getElementById('logout-item').addEventListener('click',
            () => this.sectionManager.showOnly('logout-form'));
          document.getElementById('send-data-item').addEventListener('click',
            () => this.sectionManager.showOnly('send-user-data'));
          document.getElementById('get-data-item').addEventListener('click',
            () => this.sectionManager.showOnly('get-user-data'));
          this.sectionManager.showOnly('login-form')
        }
      }

      document.addEventListener('DOMContentLoaded', (e) => {
        const app = new App();
      });
    </script>
  </body>
</html>
