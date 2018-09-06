#include "net.h"

using namespace std;

string encode(string s)
{
    for (int i = 0; i < (int)s.length(); i++) {
        if ((s[i]==' ') || (s[i]=='\r') || (s[i]=='\n')) {
            s[i] = '_'; 
        }//if
    }//for
    return s;
}

string decode(string s)
{
    for (int i = 0; i < (int)s.length(); i++) {
        if (s[i] == '_') { s[i] = ' '; }
    }//for
    return s;
}

bool isnumber(const char* istr) 
{
    if (*istr == '\0') { return false; } // empty string
    while (*istr != '\0') {
        if ( (*istr < '0') || (*istr > '9') ) {
            return false;
        }//if
        istr++;
    }//while
    return true;
}

static char seps[] = " \t\r\n";

bool Connection::readCommandFromBuffer(CommandStruct& cmd) 
{
    cmd.cmd = "";
    // extract first line
    string::size_type nlpos = acBuffer.find("\n");
    if (nlpos == string::npos) {
        return false;
    }//if
    char *bline = new char[nlpos+2];
    strncpy(bline, acBuffer.c_str(), nlpos);
    bline[nlpos] = '\0';
    acBuffer = acBuffer.substr(nlpos+1);
    

    char *bcmd = strtok(bline, seps);   // CMD
    if (bcmd == NULL) { delete[] bline;return false; } 
    cmd.cmd = string(bcmd);

    cmd.strparam = "";
    for (int j = 0; j < 8; j++) { cmd.intparams[j] = 0; }
    int i = 0;
    char *bspar = strtok(NULL, seps);// string(?) param
    if (bspar != NULL) {
        if (isnumber(bspar)) {
            cmd.intparams[0] = atoi(bspar);
            i = 1;
        } else {
            cmd.strparam = bspar;
        } //if/else
    } //if

    char *bpar = strtok(NULL, seps);    // int params
    while ( (bpar != NULL) && (i < 8) ) {
        cmd.intparams[i] = atoi(bpar);
        bpar = strtok( NULL, seps );
        i++;
    }//while
        
    delete[] bline;
    return true;
}

bool readCommandFromPlayer(PID pid, CommandStruct& cmd)
{
    for (Connections::iterator con = gConnections.begin(); con != gConnections.end(); ++con) {
        if (con->pid == pid) {
            return con->readCommandFromBuffer(cmd);
        }//
    }//for
    return false;

}

/*
string strtokline(string &str)
{
    if (str.empty()) { return ""; }
    while (str[0] == '\n') {
        str = str.substr(1, string::npos);
        if (str.empty()) { return ""; }
    }//while
    string result = "";
    string::size_type nlpos = str.find("\n");
    if (nlpos != string::npos) {
        result = str.substr(0, nlpos-1);
        str = str.substr(nlpos+1, string::npos);
    }//if
    return result;
}

string strfirstword(const string str)
{
    string::size_type spacepos = str.find(" ");
    if ((spacepos != string::npos) && (str[0] != ' ')) {
        return str.substr(0, spacepos-1);
    }//if
    return "";
}

string strparsecommand(const string str, int maxargc, int* argv)
{
	istringstream s(str);
    string str1;
    s >> str1;
    int argc = -1;
    while ((!s.eof()) && ((++argc) < maxargc)) {
        s >> argv[argc];
    }//while
    return str1;
}

string strparsecommand(const string str, string &buffer)
{
    string fw = strfirstword(str);
    buffer = str.substr(fw.length()+1, string::npos);
    return fw;
}
*/
