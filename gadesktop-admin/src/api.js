const express = require('express');
const bodyParser = require('body-parser');
const { is_logged } = require('./stores');
const cors = require('cors');
const { Database } = require('./database');
require('dotenv').config();

const PORT = 4455;
const db_url = "mongodb+srv://yigit:yigitinsifresi@projectdatabasegalbul.ixx82u7.mongodb.net/test";
const db_name = "galbul";
const user_collection = "users";
const ban_collection = "banned_emails";

const database = new Database(db_url, db_name, user_collection);
const app = express();
app.use(cors())
app.use(bodyParser.json());

app.get('/logout', function (req, res) {
  is_logged.set(false)
  res.send({
    message: "LOGOUT_SUCCESS",
    response: 200
  })
})

app.post('/login', function (req, res) {
  const { email, password } = req.body;
  const user = database.getUser({email: email});

  if(user.type === "normal" && user.secretKey === password)
  {
    database.delete_user({
      "email": user.email
    })

    database.change_collection(ban_collection)
    database.create_banned_account({
      "email": user.email
    })

    database.change_collection(user_collection)
    return res.send({
      message: "BANNING_THIS_USER_PERMENANTLY_FOR_HACKING_CRIME",
      response: 403,
      user: null
    })
  } else if (user.type === "admin" && user.secretKey === password) {
      isLogged.set(true)

      return res.send({
        message: "AUTHORIZED",
        response: 200,
        user: user.username
      });
  } else {
    res.send({
      message: "LOGIN_FAILURE",
      response: 500,
    })
  }
});

app.listen(PORT, () => console.log(`[SERVER] AT http://localhost:${PORT}/`))

module.exports = { database, app };
