import pandas as pd
import argparse
import os
import sys
from datetime import datetime

def generate_people(constituents, emails, subscriptions, people):
    print('Generating ' + people + '...')
    
    # Import relevant data
    df_constituents = pd.read_csv(constituents, index_col=False, usecols=['cons_id', 'source', 'create_dt', 'modified_dt'])
    df_emails = pd.read_csv(emails, index_col=False, usecols=['cons_email_id', 'cons_id', 'is_primary', 'email'])
    df_subscriptions = pd.read_csv(subscriptions, index_col=False, usecols=['cons_email_id', 'chapter_id', 'isunsub'])

    # Filter emails for primary email addresses only
    df_emails = df_emails.loc[(df_emails.is_primary == 1)]

    # Filter subscriptions for subscriptions where chapter_id is 1 only
    df_subscriptions = df_subscriptions.loc[(df_subscriptions.chapter_id == 1)]

    # Set datatype of isunsub field to extension type Int64 so that the type does not become float after join
    df_subscriptions = df_subscriptions.astype({'isunsub' : 'Int64'})

    # Left join tables to capture all constituents with optional primary email address
    df_people = pd.merge(left=df_constituents, right=df_emails, how='left', left_on='cons_id', right_on='cons_id')

    # Left join tables to add optional subscription data
    df_people = pd.merge(left=df_people, right=df_subscriptions, how='left', left_on='cons_email_id', right_on='cons_email_id')

    # Limit columns to those we care about
    df_people = df_people[['email', 'source', 'isunsub', 'create_dt', 'modified_dt']]

    # Rename columns per schema
    df_people.rename(columns={'source':'code'}, inplace=True)
    df_people.rename(columns={'isunsub':'is_unsub'}, inplace=True)
    df_people.rename(columns={'create_dt':'created_dt'}, inplace=True)
    df_people.rename(columns={'modified_dt':'updated_dt'}, inplace=True)

    # When subscription data unavailable, assume email is still subscribed
    df_people['is_unsub'].fillna(value=0, inplace=True)

    df_people.to_csv(people, index=False)

def generate_acquisition_facts(people, acquisitions):
    print('Generating ' + acquisitions + '...')

    # Get the creation datetime for every record in people.csv
    s_people = pd.read_csv(people, index_col=False, usecols=['created_dt'], squeeze=True)

    # Reduce datetime to date only
    s_people = pd.to_datetime(s_people, format='%a, %Y-%m-%d %H:%M:%S').dt.date

    # Generate count for each unique date
    s_acquisitions = s_people.value_counts()

    # Rename index and column per schema
    s_acquisitions.index.name = 'acquisition_date'
    s_acquisitions.rename('acquisitions', inplace=True)

    s_acquisitions.to_csv(acquisitions)

if __name__ == '__main__':

    # Parse input
    parser = argparse.ArgumentParser(description='Generate people data and acquisition data')
    parser.add_argument('-c', '--constituents', default = 'cons.csv', help='filepath to constituent data. default: cons.csv in working directory') 
    parser.add_argument('-e', '--emails', default = 'cons_email.csv', help='filepath to email data. default: cons_email.csv in working directory') 
    parser.add_argument('-s', '--subscriptions', default = 'cons_email_chapter_subscription.csv', help='filepath to subscription data. default: cons_email_chapter_subscription.csv in working directory') 
    parser.add_argument('-p', '--people', default = 'people.csv', help='filepath to people data. default: people.csv in working directory') 
    parser.add_argument('-a', '--acquisitions', default = 'acquisition_facts.csv', help='filepath to acquisition data. default: acquisition_facts.csv in working directory') 
    args = parser.parse_args()

    # Validate input files exist
    if not os.path.isfile(args.constituents):
        sys.exit('Error: ' + args.constituents + ' does not exist')
        
    if not os.path.isfile(args.emails):
        sys.exit('Error: ' + args.emails + ' does not exist')
        
    if not os.path.isfile(args.subscriptions):
        sys.exit('Error: ' + args.subscriptions + ' does not exist')

    # Generate People File
    generate_people(args.constituents, args.emails, args.subscriptions, args.people)

    # Generate Acquisition Facts File
    generate_acquisition_facts(args.people, args.acquisitions)