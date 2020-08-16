const router = require("express").Router()
const coursesController = require("../../controllers/coursesController")
const newsController = require("../../controllers/newsController")
const subscribersController = require("../../controllers/subscribersController")
const usersController = require("../../controllers/usersController")
const imagesController = require("../../controllers/imagesController")

router.post("/login", usersController.apiAuthenticate)
router.use(usersController.verifyJWT)
router.get("/subscribers", subscribersController.index, subscribersController.indexView)
router.get("/subscribers/:id/edit", subscribersController.edit)
router.put("/subscribers/:id/update", subscribersController.update, subscribersController.redirectView)
router.get("/subscribers/:id", subscribersController.show, subscribersController.showView)
router.delete("/subscribers/:id/delete", subscribersController.delete, subscribersController.redirectView)

router.post("/news/create", newsController.create, newsController.respondJSON)
router.get("/news", newsController.index, newsController.filterNews ,newsController.respondJSON)
router.put("/news/:id/update", newsController.update, newsController.respondJSON)
router.get("/news/:id", newsController.show, newsController.respondJSON)
router.delete("/news/:id/delete", newsController.delete, newsController.respondJSON)


router.get("/courses", coursesController.index,coursesController.filterUserCourses,coursesController.respondJSON)
router.get("/courses/:id/join", coursesController.join,coursesController.respondJSON)

router.post("/images/upload",imagesController.upload)
module.exports = router

