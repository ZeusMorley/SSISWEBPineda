import sys
sys.path.insert(0,"C:/laragon/bin/python/python-3.10/Scripts")
import pymysql

def create_table(mysql):
    try:
        with mysql.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS `zeusdb`.`college` (
                `CollegeCode` VARCHAR(8) NOT NULL,
                `CollegeName` VARCHAR(64) NOT NULL,
                PRIMARY KEY (`CollegeCode`),
                UNIQUE INDEX `CollegeName_UNIQUE` (`CollegeName` ASC) VISIBLE
            )""")

            cur.execute("""CREATE TABLE IF NOT EXISTS `zeusdb`.`course` (
              `CourseCode` VARCHAR(8) NOT NULL,
              `CourseName` VARCHAR(64) NOT NULL,
              `CollegeCode` VARCHAR(8) NOT NULL,
              PRIMARY KEY (`CourseCode`),
              UNIQUE INDEX `CourseName_UNIQUE` (`CourseName` ASC) VISIBLE,
              INDEX `CollegeCode_idx` (`CollegeCode` ASC) VISIBLE,
              CONSTRAINT `CollegeCode`
                FOREIGN KEY (`CollegeCode`)
                REFERENCES `zeusdb`.`college` (`CollegeCode`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION
            )""")

            cur.execute("""CREATE TABLE IF NOT EXISTS `zeusdb`.`student` (
              `StudentId` VARCHAR(9) NOT NULL,
              `StudentFirstName` VARCHAR(64) NOT NULL,
              `StudentLastName` VARCHAR(64) NOT NULL,
              `CourseCode` VARCHAR(8) NOT NULL,
              `StudentYearLvl` VARCHAR(4) NOT NULL,
              `StudentGender` VARCHAR(8) NOT NULL,
              PRIMARY KEY (`StudentId`),
              INDEX `CourseCode_idx` (`CourseCode` ASC) VISIBLE,
              CONSTRAINT `CourseCode`
                FOREIGN KEY (`CourseCode`)
                REFERENCES `zeusdb`.`course` (`CourseCode`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION
            )""")

        mysql.commit()

    except Exception as e:
        print("An error occurred:", e)
