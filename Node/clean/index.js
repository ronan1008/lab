const express = require('express')
const app = new express()
const ejs = require('ejs')
const mongoose = require('mongoose')
const bodyParser = require('body-parser')
const fileUpload = require('express-fileupload')

const newPostController = require('./controllers/newPost')
const homeController = require('./controllers/home')
const storePostController = require('./controllers/storePost')
const getPostController = require('./controllers/getPost')
const newUserController = require('./controllers/newUser')
const storeUserController = require('./controllers/storeUser')
const loginController = require('./controllers/login')
const loginUserController = require('./controllers/loginUser')
const validateMiddleware = require('./middleware/validateMiddleware')
const expressSession = require('express-session')
const authMiddleware = require('./middleware/authMiddleware')
const redirectIfAuthenticatedMiddleware = require('./middleware/redirectIfAuthenticatedMiddleware')
const logoutController = require('./controllers/logout')

app.use(express.static('public'))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({extended:true}))
app.use(fileUpload())

mongoose.connect('mongodb://localhost/my_database', {useNewUrlParser:true});

app.set('view engine','ejs')


app.listen(4000,()=>{
    console.log('App listening on port 4000')
})

app.use(expressSession({
    secret:'keyboard cat'
}))

global.loggedIn = null
app.use("*",(req,res,next)=>{
    loggedIn = req.session.userId;
    next()
});

app.get('/',homeController)
app.get('/post/:id',getPostController)
app.post('/posts/store',authMiddleware,storePostController)

app.get('/posts/new',authMiddleware,newPostController)

const customMiddleWare = (req,res,next)=>{
    console.log('Custom middle ware called')
    next()
}

app.use(customMiddleWare)
app.use('/post/store',validateMiddleware)
app.get('/auth/register',redirectIfAuthenticatedMiddleware,newUserController)
app.post('/users/register',redirectIfAuthenticatedMiddleware,storeUserController)
app.get('/auth/login',redirectIfAuthenticatedMiddleware,loginController);
app.post('/users/login',redirectIfAuthenticatedMiddleware,loginUserController)

app.get('/auth/logout',logoutController)
app.use((req,res)=>res.render('notfound'));
