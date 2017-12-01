package org.railgun.marshal;

import java.util.ArrayList;

/**
 * Created by hinus on 2017/12/1.
 */

public class BinaryFileParser {
    static int cur;
    static ArrayList<String> stringTable;

    public static CodeObject parse(byte[] sourceBytes) {
        int magicNumber; // 4 bytes;
        int modDate; // 4 bytes;
        cur = 8;
        stringTable = new ArrayList<>();

        byte objectType = sourceBytes[cur++];

        if (objectType == 'c') {
            return getCodeObject(sourceBytes);
        }

        return null;
    }

    static CodeObject getCodeObject(byte[] sourceBytes) {
        int argcount = getLong(sourceBytes);
        int nlocals = getLong(sourceBytes);
        int stacksize = getLong(sourceBytes);
        int flags = getLong(sourceBytes);

        byte[] codes = getCode(sourceBytes);

        ArrayList consts = getConsts(sourceBytes);
        ArrayList names = getNames(sourceBytes);
        ArrayList varnames = getVarNames(sourceBytes);
        ArrayList freevar = getFreeVars(sourceBytes);
        ArrayList cellvar = getCellVars(sourceBytes);
        String fileName = getFileName(sourceBytes);
        String name = getName(sourceBytes);
        int beginLineNo = getLong(sourceBytes);
        byte[] lnotab = getNoTable(sourceBytes);

        return new CodeObject(argcount, nlocals, stacksize, flags, codes,
                names, consts, varnames, freevar, cellvar,
                fileName, name, beginLineNo, lnotab);
    }

    static byte[] getNoTable(byte[] buf) {
        if (buf[cur] == 't' || buf[cur] == 's') {
            cur++;
            int length = getLong(buf);
            byte[] t = new byte[length];
            for (int i = 0; i < length; i++) {
                t[i] = buf[cur++];
            }

            return t;
        }

        return null;
    }

    static String getName(byte[] buf) {
        if (buf[cur] == 't') {
            cur++;
            String s = getString(buf);
            stringTable.add(s);
            return s;
        }
        else if (buf[cur] == 's') {
            cur++;
            return getString(buf);
        }
        else if (buf[cur] == 'R') {
            cur++;
            int index = getLong(buf);
            return stringTable.get(index);
        }

        return null;
    }

    static ArrayList getVarNames(byte[] buf) {
        if (buf[cur] == '(') {
            cur++;
            return getTuple(buf);
        }

        return null;
    }

    static ArrayList getFreeVars(byte[] buf) {
        if (buf[cur] == '(') {
            cur++;
            return getTuple(buf);
        }

        return null;
    }

    static ArrayList getCellVars(byte[] buf) {
        if (buf[cur] == '(') {
            cur++;
            return getTuple(buf);
        }

        return null;
    }

    static String getFileName(byte[] buf) {
        if (buf[cur] == 's') {
            cur++;
            return getString(buf);
        }
        else if (buf[cur] == 't') {
            cur++;
            String s = getString(buf);
            stringTable.add(s);
            return s;
        }
        else if (buf[cur] == 'R') {
            cur++;
            int index = getLong(buf);
            return stringTable.get(index);
        }

        return null;
    }

    static ArrayList getNames(byte[] buf) {
        if (buf[cur] == '(') {
            cur++;
            ArrayList list = getTuple(buf);
            return list;
        }
        return null;
    }

    static int getLong(byte[] buf) {
        int r = ((buf[cur + 3] & 0xff) << 24) |
                ((buf[cur + 2] & 0xff) << 16) |
                ((buf[cur + 1] & 0xff) << 8) |
                (buf[cur] & 0xff);
        cur += 4;
        return r;
    }

    static byte[] getCode(byte[] buf) {
        assert buf[cur] == 's';
        cur += 1;
        int length = getLong(buf);
        byte[] code = new byte[length];
        for (int i = 0; i < length; i++) {
            code[i] = buf[cur++];
        }
        return code;
    }

    static ArrayList getConsts(byte[] buf) {
        if (buf[cur] == '(') {
            cur++;
            return getTuple(buf);
        }

        return null;
    }

    public static ArrayList getTuple(byte[] buf) {
        int length = getLong(buf);
        ArrayList list = new ArrayList(length);
        for (int i = 0; i < length; i++) {
            byte objectType = buf[cur++];

            switch (objectType) {
                case 's':
                    list.add(getString(buf));
                    break;
                case 'N':
                    list.add(null);
                    break;
                case 'i':
                    list.add(getLong(buf));
                    break;
                case '(':
                    list.add(getTuple(buf));
                    break;
                case 't':
                    String s = getString(buf);
                    list.add(s);
                    stringTable.add(s);
                    break;
                case 'c':
                    list.add(getCodeObject(buf));
                    break;
                case 'R':
                    list.add(getRef(buf));
                    break;
                default:
                    throw new RuntimeException("unrecognized type: " + objectType);
            }
        }

        return list;
    }

    public static String getRef(byte[] buf) {
        int index = getLong(buf);
        return stringTable.get(index);
    }

    public static String getString(byte[] buf) {
        int length = getLong(buf);
        byte[] sbuf = new byte[length];

        for (int i = 0; i < length; i++) {
            sbuf[i] = buf[cur++];
        }

        return new String(sbuf);
    }
}
