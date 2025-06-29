declare module BBearSchema {
    interface CardTypeInfo {
        cardTypeCode: string;
        cardTypeName: string;
    }

    interface CardCategoryInfo {
        categoryCode: string;
        categoryName: string;
        categoryDesc: string;
    }

    interface CardThemeInfo {
        themeCode: string;
        themeName: string;
        themeDesc: string;
    }

    interface CardInfo extends CardTypeInfo, CardThemeInfo, CardCategoryInfo {
        cover: any;
        status: string;
        honoree: string;
        title: string;
        title: string;
        content: string;
        coverName: string;
        priority: string;
    }
}
