/// <reference path="./types/bbear-schema.d.ts" />

import ExcelJS from "exceljs";
import path from "path";
import { log, generateID } from "./utils";
import _ from "lodash";

const getSheetData = (worksheet: ExcelJS.Worksheet, rowNums?: number) => {
    if (!worksheet) {
        throw new Error("工作表对象为空");
    }

    const data: any[] = [];

    // 读取前两行

    if (rowNums) {
        for (let rowNum = 1; rowNum <= rowNums; rowNum++) {
            const row = worksheet.getRow(rowNum);
            const rowData: any[] = [];

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
        const rowData: any[] = [];
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
const generateCardTypeList = (sheetData: ExcelJS.Worksheet) => {
    const list = getSheetData(sheetData);
    const jsonList: BBearSchema.CardTypeInfo[] = list
        .slice(1)
        .reduce((a, [cardTypeCode, cardTypeName]) => {
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
const generateCardCategoryJson = (sheetData: ExcelJS.Worksheet) => {
    const list = getSheetData(sheetData);
    const jsonList: BBearSchema.CardCategoryInfo[] = list
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
const generateCardThemeList = (sheetData: ExcelJS.Worksheet) => {
    const list = getSheetData(sheetData);
    const jsonList: BBearSchema.CardThemeInfo[] = list
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
 * 第 10 列: 封面图
 * 第 11 列: 高频优先级
 * 第 12 列:
 */
const generateBBearCardList = (
    sheetData: ExcelJS.Worksheet,
    cardTypeList: BBearSchema.CardTypeInfo[],
    cardCategoryList: BBearSchema.CardCategoryInfo[],
    cardThemeList: BBearSchema.CardThemeInfo[]
) => {
    const list = getSheetData(sheetData);
    const jsonList: BBearSchema.CardInfo[] = list
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
                const { themeCode } =
                    cardThemeList.find(
                        ({ themeName: themeNameFromSheet }) =>
                            themeName === themeNameFromSheet
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

const getFieldsStrFromList = (list: any[], fields: string[]) => {
    return fields.map((field) => {
        return list.map((v) => v[field]).join(",");
    });
};

const logSomething = (
    data: {
        cardTypeList: BBearSchema.CardTypeInfo[];
        cardCategoryList: BBearSchema.CardCategoryInfo[];
        cardThemeList: BBearSchema.CardThemeInfo[];
    },
    config?: {
        showCategory?: boolean;
        showTheme?: boolean;
        showType?: boolean;
    }
) => {
    const { cardTypeList, cardCategoryList, cardThemeList } = data;
    const { showCategory, showTheme, showType } = config || {};
    if (showType) {
        log(
            `卡片类型：共 ${cardTypeList.length} 种`,
            getFieldsStrFromList(cardTypeList, ["cardTypeCode", "cardTypeName"])
        );
    }

    if (showCategory) {
        log(
            `卡片分类：共 ${cardCategoryList.length} 种`,
            getFieldsStrFromList(cardCategoryList, [
                "categoryCode",
                "categoryName",
            ])
        );
    }

    if (showTheme) {
        log(
            `卡片主题：共 ${cardThemeList.length} 种`,
            getFieldsStrFromList(cardThemeList, ["themeCode", "themeName"])
        );
    }
};

async function readExcel(filePath: string) {
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

        const cardTypeList = generateCardTypeList(cardTypeSheet);
        // console.log("=== cardTypeList ===");
        // console.log(cardTypeList);

        const cardCategoryList = generateCardCategoryJson(cardCategorySheet);
        const cardThemeList = generateCardThemeList(cardThemeSheet);
        // console.log("=== cardCategoryList ===");
        // console.log(cardCategoryList);

        const cardList = generateBBearCardList(
            cardSheet,
            cardTypeList,
            cardCategoryList,
            cardThemeList
        );

        // logSomething(
        //     {
        //         cardTypeList,
        //         cardCategoryList,
        //         cardThemeList,
        //     },
        //     {
        //         showCategory: true,
        //         showTheme: true,
        //         showType: true,
        //     }
        // );

        return cardList;
    } catch (err) {
        console.error("读取Excel出错:", err);
        throw err;
    }
}

async function testParseBBearCardXlsx() {
    try {
        // 使用示例
        console.log("=== 开始解析 ===");
        const dirpath = path.join(__dirname, "b_bear_card.xlsx");
        const cards = await readExcel(dirpath);
        // log("卡片数据", cards);
    } catch (err) {
        console.log("=== 解析错误 ===");
        console.error(err);
    }
}

async function getCardsFromBBearCardExcel() {
    try {
        log(`=== 开始处理 getCardsFromBBearCardExcel ===`);
        const dirpath = path.join(__dirname, "b-bear-card.xlsx");
        const cards = await readExcel(dirpath);

        log(`卡片数据: 共 ${cards.length} 条`);
        return cards;
    } catch (err) {
        console.log("=== 解析错误 ===");
        console.error(err);
    }
}

export { getCardsFromBBearCardExcel, testParseBBearCardXlsx };
