# life.py

import argparse
import pendulum
import sys

from fpdf import FPDF
from colorama import init, Fore
from typing import List

init()

SUPPORTED_DATE_FORMATS = ['YYYY-MM-DD']


def parse_date(date: str):
    for f in SUPPORTED_DATE_FORMATS:
        try:
            res = pendulum.from_format(date, fmt=f)
        except ValueError:
            continue
        else:
            return res
    raise ValueError(
        f'Incorrect date format. Please specify date in any of the below formats\n {", ".join(SUPPORTED_DATE_FORMATS)}'
    )


def parse_args(args: List[str]):
    parser = argparse.ArgumentParser(__name__)

    parser.add_argument(dest='dob', type=parse_date, help='date of birth')
    parser.add_argument(
        '-s',
        dest='span',
        type=int,
        default=80,
        help='lifespan in years: defaults to 80',
    )
    parser.add_argument(
        '-o', 
        dest='file_name',
        default='life_in_weeks.pdf',
        help= 'output file name'
    )
    res = parser.parse_args()
    return res


def create_calendar(start_date: pendulum.DateTime):
    end_date = start_date.add(args.span)
    weeks = end_date.diff(start_date).in_weeks()

    birthdays = (start_date.add(years=i).date() for i in range(args.span))
    next_birthday = next(birthdays)
    for week in range(1, weeks + 1):
        week_start = start_date.add(weeks=week - 1).date()
        week_end = start_date.add(weeks=week, days=-1).date()

        msg = f"Week: {week:04} Start: {week_start} End: {week_end}"

        # highlight the birthday week
        if next_birthday >= week_start and next_birthday <= week_end:
            print(f"{Fore.GREEN}{msg}")
            try:
                next_birthday = next(birthdays)
            except StopIteration:
                pass

        print(f"{Fore.WHITE}{msg}")

def create_pdf(file_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(240)
    width, height, dx, dy = 3, 3, 1, 2
    RECT_PER_ROW = 50
    
    # increment from previously drawn shape to adjust rectangle drawing
    incr_from_prev = dx
    y = 20
    for i in range(500*5):
        if i % RECT_PER_ROW == 0:
            y = y + height + dy
            incr_from_prev = width + dx # add width to align with previous row
        x = width * ( i % RECT_PER_ROW ) + incr_from_prev
        pdf.rect(x=x, y=y, w=width, h=height)
        incr_from_prev += dx
    pdf.output(file_name)

def main(args):
    #create_calendar(args.dob)
    create_pdf(args.file_name)


if __name__ == "__main__":
    args = parse_args(sys.argv)
    main(args)
