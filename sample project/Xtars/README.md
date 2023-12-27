Robot Framework
=============

Project Structure
------------
* tests
   1. Test Case 的集合
   2. 底下可以建立資料夾，例如 : My Backpack 針對背包的 Case
* Resources
   1. 可重複使用的關鍵字
   2. 例如  登入、登出
* Libraries
   1. .py 檔案也可以放在這
* Settings
   1. 變數放置

Requirements
------------
* 創建虛擬環境
  1. pip3 install virtualenv
  2. cd /Users/leechenghan/Developer
  3. virtualenv robot_env
  4. cd robot_env
  5. source ./bin/activate
* 在虛擬環境中，安裝 python 套件
  1. cd /Users/leechenghan/Developer/tl-QA/Mobile_Automation/Xtars
  2. pip install -r requirements.txt
* 退出虛擬環境
  1. deactivate
* 刪除虛擬環境
  1. rm -rf robot_env/

Common
--------------

* <span style="color:#A53D3D"> <strong>Tags And Folders</strong> </span>
    ```console
    robot --outputdir $HOME/Documents/xtarsReport/ --timestampoutputs -i rat iOS/
    ```

Execute Assigned Tag
--------------
* <span style="color:grey"> <strong>Basic Usage</strong> </span>
    ```console
    robot [File.robot] or [robotFolder]
    ```

* <span style="color:#3A8732"> <strong>Include Tags</strong> </span>
    ```console
    robot -i rat iOS/
    ```

* <span style="color:#A53D3D"> <strong>Exclude Tags</strong> </span>
    ```console
    robot -e rat iOS/
    ```

Execute And Assigned Report Folder
--------------
* <span style="color:grey"> <strong>Basic Usage</strong> </span>
    ```console
    robot --outputdir $HOME/TestReport/Android --timestampoutputs
    ```