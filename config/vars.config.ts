export const DATA_SOURCES = {
    mySqlDataSource: {
      DB_HOST: "127.0.0.1",
      DB_USER: "root",
      DB_PASSWORD: "111111",
      DB_PORT: "3306",
      DB_DATABASE: "hc_fcg",
      DB_CONNECTION_LIMIT: process.env.MY_SQL_DB_CONNECTION_LIMIT ? parseInt(process.env.MY_SQL_DB_CONNECTION_LIMIT) : 4,
    }
};
  

