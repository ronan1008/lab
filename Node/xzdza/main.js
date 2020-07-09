const express = require("express")
const app = express()
const homeController = require("./controllers/homeController")
const errorController = require("./controllers/errorController")
const subscribersController = require("./controllers/subscribersController")
const usersController = require("./controllers/usersController.js")
const coursesController = require("./controllers/coursesController")
const layouts = require("express-ejs-layouts")
const mongoose = require("mongoose")
const mehtodOveride = require("method-override")
const passport = require("passport")
const cookieParser = require("cookie-parser")
const expressSession = require("express-session")
const User = require("./models/user")
const router = express.Router()
const connectFlash = require("connect-flash")
const expressValidator = require("express-validator")
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
router.use(connectFlash())
router.use(passport.initialize())
router.use(passport.session())
router.use(expressValidator())

passport.use(User.createStrategy())
passport.serializeUser(User.serializeUser())
passport.deserializeUser(User.deserializeUser())

router.use((req, res, next) => {
    res.locals.loggedIn = req.isAuthenticated()
    res.locals.currentUser = req.user
    res.locals.flashMessages = req.flash()
    next()
})

router.get("/", homeController.index);

router.get("/users", usersController.index, usersController.indexView);
router.get("/users/new", usersController.new);
router.post("/users/create", usersController.validate, usersController.create, usersController.redirectView);
router.get("/users/login", usersController.login)
router.post("/users/login", usersController.authenticate)
router.get("/users/logout", usersController.logout, usersController.redirectView)
router.get("/users/:id/edit", usersController.edit);
router.put("/users/:id/update", usersController.update, usersController.redirectView);
router.get("/users/:id", usersController.show, usersController.showView);
router.delete("/users/:id/delete", usersController.delete, usersController.redirectView);

router.get("/subscribers", subscribersController.index, subscribersController.indexView)
router.get("/subscribers/new", subscribersController.new)
router.post("/subscribers/create", subscribersController.create, subscribersController.redirectView)
router.get("/subcribers/:id/edit", subscribersController.edit)
router.put("/subscribers/:id/update", subscribersController.update, subscribersController.redirectView)
router.get("/subscribers/:id", subscribersController.show, subscribersController.showView)
router.delete("/subscribers/:id/delete", subscribersController.delete, subscribersController.redirectView)

router.get("/courses", coursesController.index, coursesController.indexView);
router.get("/courses/new", coursesController.new);
router.post("/courses/create", coursesController.create, coursesController.redirectView);
router.get("/courses/:id/edit", coursesController.edit);
router.put("/courses/:id/update", coursesController.update, coursesController.redirectView);
router.get("/courses/:id", coursesController.show, coursesController.showView);
router.delete("/courses/:id/delete", coursesController.delete, coursesController.redirectView);


router.use(errorController.pageNotFoundError)
router.use(errorController.internalServerError)

app.use("/", router)

app.listen(app.get("port"), ()=> {
    console.log(`Server run at http://localhost:${app.get('port')}`)
})

db.once("open", () => {
    console.log("Successfully connected to DB")
})