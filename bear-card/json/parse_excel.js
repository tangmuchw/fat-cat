const ExcelJS = require("exceljs");
const path = require("path");
const { generateID } = require("./utils");
const _ = require("lodash");

const getSheetData = (worksheet, rowNums) => {
    if (!worksheet) {
        throw new Error("工作表对象为空");
    }

    const data = [];

    // 读取前两行

    if (rowNums) {
        for (let rowNum = 1; rowNum <= rowNums; rowNum++) {
            const row = worksheet.getRow(rowNum);
            const rowData = [];

            // 获取所有单元格数据
            row.eachCell({ includeEmpty: true }, (cell) => {
                rowData.push(cell.value);
            });

            data.push(rowData);
        }

        return data;
    }

    // 遍历所有行（不包括空行）
    worksheet.eachRow({ includeEmpty: false }, (row, rowNumber) => {
        const rowData = [];
        // 遍历单元格
        row.eachCell({ includeEmpty: true }, (cell) => {
            rowData.push(cell.value);
        });
        data.push(rowData);
    });

    return data;
};

/**
 * 第 1 列: 卡类型编码
 * 第 2 列: 卡类型名称
 */
const generateCardTypeJson = (sheetData) => {
    const list = getSheetData(sheetData);
    const jsonList = list.slice(1).reduce((a, [cardTypeCode, cardTypeName]) => {
        return [
            ...a,
            {
                cardTypeCode,
                cardTypeName,
            },
        ];
    }, []);

    return jsonList;
};

/**
 * 第 1 列: 卡分类编码
 * 第 2 列: 卡分类名称
 * 第 3 列: 卡分类描述
 */
const generateCardCategoryJson = (sheetData) => {
    const list = getSheetData(sheetData);
    const jsonList = list
        .slice(1)
        .reduce((a, [categoryCode, categoryName, categoryDesc]) => {
            return [
                ...a,
                {
                    categoryCode,
                    categoryName,
                    categoryDesc,
                },
            ];
        }, []);

    return jsonList;
};

/**
 * 第 1 列: 卡主题编码
 * 第 2 列: 卡主题名称
 * 第 3 列: 卡主题描述
 */
const generateCardThemeJson = (sheetData) => {
    const list = getSheetData(sheetData);
    const jsonList = list
        .slice(1)
        .reduce((a, [themeCode, themeName, themeDesc]) => {
            return [
                ...a,
                {
                    themeCode,
                    themeName,
                    themeDesc,
                },
            ];
        }, []);

    return jsonList;
};

/**
 * 第 1 列: 一级分类名称
 * 第 2 列: 一级分类描述
 * 第 3 列: 卡片类型名称
 * 第 4 列: 主题名称
 * 第 5 列: 致敬对象
 * 第 6 列: 标题
 * 第 7 列: 正文
 * 第 8 列: 封面设计描述
 * 第 9 列: 封面尺寸
 * 第 10 列: 高频优先级
 * 第 11 列: 主题编码
 */
const generateCardJson = (sheetData, cardTypeList, cardCategoryList) => {
    const list = getSheetData(sheetData);
    const jsonList = list
        .slice(1)
        .reduce(
            (
                a,
                [
                    categoryName,
                    categoryDesc,
                    cardTypeName,
                    themeName,
                    honoree,
                    title,
                    content,
                    coverDesignDesc,
                    coverDesignStyle,
                    coverSize,
                    coverName,
                    priority,
                    themeCode,
                ]
            ) => {
                const { cardTypeCode } =
                    cardTypeList.find(
                        ({ cardTypeName: cardTypeNameFromSheet }) =>
                            cardTypeName === cardTypeNameFromSheet
                    ) || {};
                const { categoryCode } =
                    cardCategoryList.find(
                        ({ categoryName: categoryNameFromSheet }) =>
                            categoryName === categoryNameFromSheet
                    ) || {};
                const idParams = {
                    cardTypeCode,
                    categoryCode,
                    themeCode,
                };
                return [
                    ...a,
                    {
                        _id: `${cardTypeCode}-${generateID(idParams)}`,
                        categoryCode,
                        categoryName,
                        // categoryDesc,
                        typeCode: cardTypeCode,
                        typeName: cardTypeName,
                        themeName,
                        themeCode,
                        cover: coverName,
                        honoree,
                        title,
                        content,
                        // coverDesignDesc,
                        // coverSize,
                        priority,
                    },
                ];
            },
            []
        );

    return jsonList;
};

async function readExcel(filePath) {
    const workbook = new ExcelJS.Workbook();

    try {
        // 读取文件
        await workbook.xlsx.readFile(filePath);

        // 获取第一个工作表
        const cardTypeSheet = workbook.getWorksheet("卡类型");
        const cardCategorySheet = workbook.getWorksheet("卡分类");
        const cardSheet = workbook.getWorksheet("卡片");
        const cardThemeSheet = workbook.getWorksheet("主题");

        // 添加空值检查
        if (
            !cardTypeSheet ||
            !cardCategorySheet ||
            !cardSheet ||
            !cardThemeSheet
        ) {
            throw new Error("工作表不存在，请检查Excel文件结构");
        }

        const cardTypeList = generateCardTypeJson(cardTypeSheet);
        // console.log("=== cardTypeList ===");
        // console.log(cardTypeList);

        const cardCategoryList = generateCardCategoryJson(cardCategorySheet);
        const cardThemeList = generateCardThemeJson(cardThemeSheet);
        // console.log("=== cardCategoryList ===");
        // console.log(cardCategoryList);

        const cardList = generateCardJson(
            cardSheet,
            cardTypeList,
            cardCategoryList
        );

        // console.log("=== cardCategoryList name ===");
        // console.log(
        //     cardCategoryList
        //         .map(
        //             ({ categoryCode, categoryName }) =>
        //                 `${categoryCode} ${categoryName}`
        //         )
        //         .join(", ")
        // );

        // console.log("=== cardCategoryList code ===");
        // console.log(
        //     cardCategoryList.reduce(
        //         (a, { categoryCode }) => `${a}|"${categoryCode}"`,
        //         ""
        //     )
        // );

        // console.log("=== cardTypeList name ===");
        // console.log(
        //     cardTypeList
        //         .map(
        //             ({ cardTypeName, cardTypeCode }) =>
        //                 `${cardTypeCode} ${cardTypeName}`
        //         )
        //         .join(", ")
        // );

        console.log("=== cardTypeList code ===");
        console.log(
            cardTypeList
            // cardTypeList.reduce(
            //     (a, { cardTypeCode }) => `${a}, ${cardTypeCode}`,
            //     ""
            // )
        );

        // console.log("=== cardThemeList name ===");
        // console.log(
        //     cardThemeList
        //         .map(({ themeCode, themeName }) => `${themeCode} ${themeName}`)
        //         .join(", ")
        // );

        // console.log("=== cardThemeList code ===");
        // console.log(
        //     cardThemeList.reduce(
        //         (a, { themeCode }) => `${a}|"${themeCode}"`,
        //         ""
        //     )
        // );
        // const d1 = cardCategoryList.reduce(
        //     (a, { categoryCode, categoryName }) => {
        //         return {
        //             ...a,
        //             [categoryCode]: {
        //                 iconType: "",
        //                 desc: categoryName,
        //             },
        //         };
        //     },
        //     {}
        // );

        // const d2 = cardTypeList.reduce((b, { cardTypeCode, cardTypeName }) => {
        //     return {
        //         ...b,
        //         [cardTypeCode]: {
        //             iconType: "",
        //             desc: `${cardTypeName}`,
        //         },
        //     };
        // }, {});

        // // const d2 = cardTypeList.map(({ cardTypeCode }) => [cardTypeCode, ""]);
        // console.log("=== d1,d2 ===");
        // console.log({ ...d1, ...d2 });

        return cardList;
    } catch (err) {
        console.error("读取Excel出错:", err);
        throw err;
    }
}

async function main() {
    try {
        // 使用示例
        console.log("=== 开始解析 ===");
        const dirpath = path.join(__dirname, "b_bear_card.xlsx");
        const cards = await readExcel(dirpath);
        console.log("=== 卡片数据 ===");
        console.log(cards);
    } catch (err) {
        console.log("=== 解析错误 ===");
        console.error(err);
    }
}

// main();

const generateCardThemes = (cards) => {
    const themes = cards.map(({ themeCode, themeName }) => ({
        themeCode,
        themeName,
    }));
    const uniqueThemes = _.uniqBy(themes, "themeCode");

    console.log("=== 卡主题 ===");
    console.log(uniqueThemes);
};

async function getCardsFromBBearCardExcel() {
    try {
        // 使用示例
        console.log("=== 开始解析 getCardsFromBBearCardExcel ===");
        const dirpath = path.join(__dirname, "b_bear_card.xlsx");
        const cards = await readExcel(dirpath);

        // generateCardThemes(cards);
        console.log(`=== 卡片数据: 共 ${cards.length} 条 ===`);
        // console.log(cards);
        return cards;
    } catch (err) {
        console.log("=== 解析错误 ===");
        console.error(err);
    }
}

// getCardsFromBBearCardExcel();
// node ./parse_excel.js
module.exports = {
    getCardsFromBBearCardExcel,
};
