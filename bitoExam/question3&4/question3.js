function multiplyAndSort(arr) {
    // 驗證並相乘
    const results = arr.map(subArr => subArr[0] * subArr[1] === subArr[2]);

    // 檢查是否全部通過驗證
    if (results.every(result => result)) {
      // 提取相乘的結果並排序
      const multipliedValues = arr.map(subArr => subArr[0] * subArr[1]);
      sort_arr = arr.flat().sort((a, b) => a - b)
      return sort_arr;
    } else {
      console.log("有些驗證未通過，請檢查array。");
      return null;
    }
  }

  // 測試
  const numberList = [
    [20, 0.3, 6],
    [5, 2, 10],
    [1, 4, 4]
  ];

  const result = multiplyAndSort(numberList);

  if (result !== null) {
    console.log("通過驗證的結果並排序:", result);
  }
