const router = require("express").Router()
const userRoutes = require("./userRoutes")
const subscriberRoutes = require("./subscriberRoutes")
const courseRoutes = require("./courseRoutes")
const errorRoutes = require("./errorRoutes")


router.use("/users", userRoutes)
router.use("/subscribers", subscriberRoutes)
router.use("/courses", courseRoutes)
router.use("/", errorRoutes)

module.exports = router