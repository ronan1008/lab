const router = require("express").Router()
const usersController = require("../../controllers/usersController")


router.get("/" ,usersController.index, usersController.respondJSON);
router.get("/new", usersController.new);
router.post("/create", usersController.validate, usersController.create, usersController.redirectView);
router.get("/logout", usersController.logout, usersController.redirectView)
router.put("/:id/update", usersController.update, usersController.redirectView);
router.get("/:id", usersController.show, usersController.showView);
router.delete("/:id/delete", usersController.delete, usersController.redirectView);

module.exports = router