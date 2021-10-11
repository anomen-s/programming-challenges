package com.github.fasterxml.aaltoxml.issue73;


import java.io.InputStream;

import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamConstants;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamReader;

import org.codehaus.stax2.XMLInputFactory2;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class StaxTest {

    /**
     * returns offset of last element
     * @param fileName
     * @return
     * @throws XMLStreamException
     */
    private int test(String fileName) throws XMLStreamException {
        InputStream is = this.getClass().getClassLoader().getResourceAsStream(fileName);

        XMLInputFactory factory = XMLInputFactory2.newInstance();
        factory.setProperty(XMLInputFactory2.P_PRESERVE_LOCATION, true);
        final XMLStreamReader parser = factory.createXMLStreamReader(is);

        int offset = 0;
        while (parser.hasNext()) {
            int event = parser.next();
            switch (event) {
                case XMLStreamConstants.START_ELEMENT:
                    offset = parser.getLocation().getCharacterOffset();
                    System.out.printf("--start %X:%s\n", offset, parser.getLocalName());
                    break;
                default:
                    break;
            }
        }
        return offset;
    }

    @Test
    public void testBasic() throws XMLStreamException {

        Assertions.assertEquals(0x197, test("sample.xml"));
    }

    @Test
    public void testUtf8() throws XMLStreamException {

        Assertions.assertEquals(0x1D6, test("sample-utf8.xml"));
    }

    @Test
    public void testIso() throws XMLStreamException {
        // fails - <?xml ..?> is not counted?
        Assertions.assertEquals(0x1EC, test("sample-iso-8859-2.xml"));
    }

    @Test
    public void testUtf16() throws XMLStreamException {

        Assertions.assertEquals(0x360/2, test("sample-utf16.xml"));
    }

    @Test
    public void testUtf16Space() throws XMLStreamException {

        Assertions.assertEquals(0x36C/2, test("sample-utf16-space.xml"));
    }

    @Test
    public void testUtf16Bom() throws XMLStreamException {

        Assertions.assertEquals(0x362/2, test("sample-utf16-bom.xml"));
    }

    @Test
    public void testUtf16BomNoProlog() throws XMLStreamException {

        // this passes - when counting chars, not bytes and excluding BOM
//        Assertions.assertEquals((0x312-2)/2, test("sample-utf16-bom-no-prolog.xml"));

        Assertions.assertEquals(0x312/2, test("sample-utf16-bom-no-prolog.xml"));

    }



}
