import { isLogged } from './store';
import { express } from 'express'
import { bodyParser } from 'body-parser';
import Database from './database'

const db_url = process.env.DB_URI || "";
const db_name = "galbul";
const collection_name = "users";

const database = new Database(db_url, db_name, collection_name);
const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.post('/login', function (req, res, next) {
  const { username, password } = req.body;

  const user = database.getUser({username: username});
  if(user.type === "normal")
  {
    return res.send({
      message: "UN_AUTHORIZED",
      response: 403,
      user: null
    })
  } else {
    if (user.secretKey === password)
    {
      isLogged.set(true)

      return res.send(JSON.stringify({
        message: "AUTHORIZED",
        response: 200,
        user: username
      }))
    }
  }
});