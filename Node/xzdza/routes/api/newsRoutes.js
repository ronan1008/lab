const router = require("express").Router()
const newsController = require("../../controllers/newsController")

router.post("/create", newsController.create, newsController.respondJSON)
router.get("/", newsController.index, newsController.respondJSON)
router.get("/:id", newsController.show, newsController.respondJSON)
router.put("/:id/update", newsController.update, newsController.respondJSON)
router.delete("/:id/delete", newsController.delete, newsController.respondJSON)

module.exports = router
