const express = require("express")
const app = express()
const layouts = require("express-ejs-layouts")
const mongoose = require("mongoose")
const mehtodOveride = require("method-override")
const passport = require("passport")
const cookieParser = require("cookie-parser")
const expressSession = require("express-session")
const User = require("./models/user")
const connectFlash = require("connect-flash")
const expressValidator = require("express-validator")
const router = require("./routes/index")
mongoose.connect("mongodb://localhost:27017/xzdza", 
                    {
                        useNewUrlParser: true,
                        useUnifiedTopology: true,
                        useCreateIndex: true,
                        useFindAndModify: false
                    }
                )
const db = mongoose.connection



app.set("view engine", "ejs")
app.set("port", process.env.PORT || 3000)

router.use(
    mehtodOveride("_method",{
        methods: ["POST","GET"]
    })
)
router.use(express.urlencoded({extended: false}))
router.use(express.json())
router.use(layouts)
router.use(express.static("public"))
router.use(cookieParser("SecretCuisine123"))
router.use(expressSession({
    secret: "secretCuisine123",
    cookie: {
        maxAge: 4000000
    },
    resave: false,
    saveUninitialized: false
}))
app.use(connectFlash())
app.use(passport.initialize())
app.use(passport.session())
app.use(expressValidator())

passport.use(User.createStrategy())
passport.serializeUser(User.serializeUser())
passport.deserializeUser(User.deserializeUser())

app.use((req, res, next) => {
    res.locals.loggedIn = req.isAuthenticated()
    res.locals.currentUser = req.user
    res.locals.flashMessages = req.flash()
    next()
})

app.use("/", router)

app.listen(app.get("port"), ()=> {
    console.log(`Server run at http://localhost:${app.get('port')}`)
})

db.once("open", () => {
    console.log("Successfully connected to DB")
})