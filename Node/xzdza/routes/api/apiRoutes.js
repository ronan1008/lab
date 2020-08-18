const router = require("express").Router()
const userRoutes = require("./userRoutes")
const subscriberRoutes = require("./subscriberRoutes")
const courseRoutes = require("./courseRoutes")
const newsRoute = require("./newsRoutes")
const errorRoutes = require("./errorRoutes")
const adminRoute = require("./adminRoutes")


router.use("/users", userRoutes)
router.use("/news", newsRoute)
router.use("/subscribers", subscriberRoutes)
router.use("/courses", courseRoutes)
router.use("/admin", adminRoute)
//router.use("/", errorRoutes)

module.exports = router

