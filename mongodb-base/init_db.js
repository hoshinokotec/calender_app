db = db.getSiblingDB('db_calender');

db.db_calender.insertMany([
    {
        content: 'event1',
        event_id: 1,
        created_date: new Date(),
        alterted_date: null,
        completed_date: null
    },
    {
        content: 'event2',
        event_id: 2,
        created_date: new Date(),
        alterted_date: null,
        completed_date: null
    }
]);

