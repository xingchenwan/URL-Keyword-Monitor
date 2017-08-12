import urllib2
import os
import time
import re

keywords = ["Quick", "Fox", "jumps", "over", "lazy", "dog"]
URL = 'http://some.website'
file_name = 'urlmonitor.txt'


def internet_test():
    print 'Testing Connection...'
    req = urllib2.Request(URL)
    try:
        urllib2.urlopen(req)
    except urllib2.URLError, e:
        print e.reason
        return False
    print 'OK'
    return True


def check_param(length_buffer=False, max_length=None):
    """ Check whether the parameters (URL and Keywords) of the current run are the same as the earlier trials.
    If not, the file will be cleared and replaced with a new one to avoid false results """
    print 'Checking parameter consistency...'
    line_no = -2
    try:
        open(file_name, 'a')
    except IOError:
        return

    if os.path.getsize(file_name):
        for line in open(file_name):
            if line_no < 0:
                if line.find(URL) == -1 and line_no == -2:  # For first line: URL line
                    print 'URL inconsistency found. Clearing file now'
                    os.remove(file_name)
                    return
                else:
                    pass
            elif line_no > len(keywords) - 1:
                pass
            elif line.find(keywords[line_no]) == -1:
                print 'Keyword inconsistency found. Clearing file now'
                os.remove(file_name)
                return
            line_no += 1
    if line_no > max_length and length_buffer:
        print 'File length is too big. Clearing old contents now'
        os.remove(file_name)
        return
    print 'OK'
    return


def write_file(incidences):
    """Append/write result for this execution to the file"""
    f = open(file_name, 'a')
    if not os.path.getsize(file_name):
        f.write('{0:s}\n'.format(URL))
    f.write('{0:s}\n'.format(time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())))
    for index in range(0, len(incidences)):
        f.write("%s===%s\n" % (keywords[index], str(incidences[index])))


def match(line_no):
    """Takes line_no and returns the corresponding appropriate keyword index to be matched"""
    if not line_no:
        return -2  # URL Line
    else:
        if not line_no % (len(keywords) + 1):
            return len(keywords) - 1
        elif line_no % (len(keywords) + 1) != 1:
            return line_no % (len(keywords) + 1) - 2
        else:
            return -1


def main(verbose=False, notif_email=True):
    is_changed = False
    response = urllib2.urlopen(URL).read()
    check_param()
    f = open(file_name, 'a+')
    incidences = [response.count(keyword) for keyword in keywords]
    print 'Comparing texts...'
    print 'No previous version found. File Created' if not os.path.getsize(
        file_name) else 'Previous version found\nChecking for changes...'
    line_count = 0
    for line in open(file_name):
        if match(line_count) == -2:
            pass
        elif match(line_count) == -1:
            time_line = line
        else:
            m = re.search('===', line)
            if int(line[m.start() + len('==='):]) != incidences[match(line_count)]:
                if verbose: print (line[m.start() + len('===')], incidences[match(line_count)])
                print (
                    'Done.\n\nChanges found by comparing the current web page and the version retrieved at {0:s}'
                    'for keyword "{1:s}":\n'
                    '(Original Value: {2:d}, Current Value: {3:d})\n\n'
                    'Please go to the page {4:s} to review changes'.format(time_line, keywords[match(line_count)],
                                                                           int(line[m.start() + len('==='):]),
                                                                           incidences[match(line_count)],
                                                                           URL))
                is_changed = True
                if notif_email:
                    print ("Sending Email...")
                    email(keywords[match(line_count)])
                    print ('Success!')
                break
        line_count += 1
    if not is_changed: print "Done. No changes found"
    write_file(incidences)
    return


def email(keyword):
    import smtplib
    server = smtplib.SMTP('smtp.live.com', 587)
    server.ehlo()
    server.starttls()
    server.login('email', 'pass')
    message = "\r\n".join([
        "From: Automated Alert",
        "To: Your name",
        "Subject: Webpage change - Alert",
        'A change in keywords in watched webpage is detected at URL : {0:s}'
        ' for keyword "{1:s}"'.format(URL, keyword)])
    # server.set_debuglevel(1)
    server.sendmail('send', 'receive', message)
    server.quit()


if __name__ == '__main__':
    if internet_test():
        main()
