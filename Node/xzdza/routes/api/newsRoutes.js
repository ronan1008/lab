const router = require("express").Router()
const newsController = require("../../controllers/newsController")


router.get("/", newsController.frontIndex, newsController.respondJSON)
router.get("/:id", newsController.show, newsController.respondJSON)
router.put("/:id/update", newsController.update, newsController.respondJSON)
router.delete("/:id/delete", newsController.delete, newsController.respondJSON)

module.exports = router
