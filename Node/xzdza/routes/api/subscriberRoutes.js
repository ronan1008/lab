
const router = require("express").Router()
const subscribersController = require("../../controllers/subscribersController")
const usersController = require("../../controllers/usersController")

router.post("/create", subscribersController.create, subscribersController.redirectView)

router.use(usersController.verifyJWT)
router.get("/", subscribersController.index, subscribersController.indexView)
router.get("/new", subscribersController.new)
router.put("/:id/update", subscribersController.update, subscribersController.redirectView)
router.get("/:id", subscribersController.show, subscribersController.showView)
router.delete("/:id/delete", subscribersController.delete, subscribersController.redirectView)

module.exports = router