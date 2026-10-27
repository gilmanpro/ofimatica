const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, ExternalHyperlink } = require('docx');
const fs = require('fs');

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Arial", size: 20 } // 10pt - letra mas pequena
      }
    },
    paragraphStyles: [
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 24, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 100, after: 60 }, outlineLevel: 0 }
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 22, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 80, after: 40 }, outlineLevel: 1 }
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 } // margenes mas pequenos
      }
    },
    children: [
      // TITULO
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "Aportes de Alan Turing e Impacto en la Actualidad", bold: true })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 120 },
        children: [new TextRun({ text: "Su relacion con la Mineria de Datos", size: 18, italics: true })]
      }),

      // APORTES
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun({ text: "Aportes Fundamentales" })]
      }),
      new Paragraph({
        spacing: { after: 60 },
        children: [new TextRun({ text: "Alan Turing (1912-1954) fue el padre de la ciencia de la computacion teorica. Sus principales aportes:" })]
      }),
      new Paragraph({
        spacing: { after: 40 },
        children: [new TextRun({ text: "- Mquina de Turing (1936): ", bold: true }), new TextRun({ text: "Modelo teorico que fundo la computacion digital moderna." })]
      }),
      new Paragraph({
        spacing: { after: 40 },
        children: [new TextRun({ text: "- Rompimiento de Enigma: ", bold: true }), new TextRun({ text: "Desarrollo la maquina Bombe, acortando la guerra y salvando millones de vidas." })]
      }),
      new Paragraph({
        spacing: { after: 40 },
        children: [new TextRun({ text: "- Test de Turing (1950): ", bold: true }), new TextRun({ text: "Criterio para evaluar inteligencia artificial." })]
      }),
      new Paragraph({
        spacing: { after: 80 },
        children: [new TextRun({ text: "- Pionero de IA: ", bold: true }), new TextRun({ text: "Precursor directo del machine learning y los sistemas modernos de IA." })]
      }),

      // IMPACTO
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun({ text: "Impacto Actual" })]
      }),
      new Paragraph({
        spacing: { after: 60 },
        children: [new TextRun({ text: "Su vision permea toda nuestra vida digital: computadoras, smartphones, asistentes virtuales (ChatGPT), mineria de big data y ciberseguridad." })]
      }),

      // PREGUNTAS
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun({ text: "Respuestas" })]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun({ text: "1. Como encontrar informacion util en datos incomprensibles?", size: 20 })]
      }),
      new Paragraph({
        spacing: { after: 60 },
        children: [new TextRun({ text: "Los procesos mecanicos de Turing demuestran que datos aparentemente caoticos revelan estructura mediante reglas sistematicas. Los patrones emergen al procesar grandes volumenes con algoritmos consistentes." })]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun({ text: "2. Relación con la miner\u00EDa de datos?", size: 20 })]
      }),
      new Paragraph({
        spacing: { after: 60 },
        children: [new TextRun({ text: "Turing sento las bases: sus tecnicas de criptoanalsis para encontrar patrones ocultos en mensajes cifrados son precursoras directas de los algoritmos modernos de minera de datos. La maquina universal permite procesar cualquier dato para descubrir conocimiento." })]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun({ text: "3. Estrategias de Turing para mensajes cifrados?", size: 20 })]
      }),
      new Paragraph({
        spacing: { after: 80 },
        children: [new TextRun({ text: "Desarroll\u00F3: an\u00E1lisis estad\u00EDstico de frecuencias, Banburismo (t\u00E9cnica probabil\u00EDstica), explotaci\u00F3n de errores humanos, Cribs (informaci\u00F3n probable), Turingery e ingenier\u00EDa inversa." })]
      }),

      // REFERENCIAS
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun({ text: "Referencias" })]
      }),
      new Paragraph({
        spacing: { after: 30 },
        children: [
          new TextRun({ text: "[1] " }),
          new ExternalHyperlink({
            children: [new TextRun({ text: "https://en.wikipedia.org/wiki/Alan_Turing", style: "Hyperlink", size: 18 })],
            link: "https://en.wikipedia.org/wiki/Alan_Turing"
          })
        ]
      }),
      new Paragraph({
        spacing: { after: 30 },
        children: [
          new TextRun({ text: "[2] " }),
          new ExternalHyperlink({
            children: [new TextRun({ text: "https://www.britannica.com/biography/Alan-Turing", style: "Hyperlink", size: 18 })],
            link: "https://www.britannica.com/biography/Alan-Turing"
          })
        ]
      }),
      new Paragraph({
        spacing: { after: 30 },
        children: [
          new TextRun({ text: "[3] " }),
          new ExternalHyperlink({
            children: [new TextRun({ text: "https://plato.stanford.edu/entries/turing/", style: "Hyperlink", size: 18 })],
            link: "https://plato.stanford.edu/entries/turing/"
          })
        ]
      }),
      new Paragraph({
        spacing: { after: 30 },
        children: [
          new TextRun({ text: "[4] " }),
          new ExternalHyperlink({
            children: [new TextRun({ text: "https://www.iwm.org.uk/history/second-world-war/how-alan-turing-cracked-the-enigma-code", style: "Hyperlink", size: 18 })],
            link: "https://www.iwm.org.uk/history/second-world-war/how-alan-turing-cracked-the-enigma-code"
          })
        ]
      }),
      new Paragraph({
        spacing: { after: 60 },
        children: [
          new TextRun({ text: "[5] " }),
          new ExternalHyperlink({
            children: [new TextRun({ text: "https://www.britannica.com/technology/artificial-intelligence", style: "Hyperlink", size: 18 })],
            link: "https://www.britannica.com/technology/artificial-intelligence"
          })
        ]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 60 },
        children: [new TextRun({ text: "\"La filosofia de Turing pervive en cada busqueda y sistema inteligente actual.\"", italics: true, size: 18 })]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("Trabajo_Alan_Turing.docx", buffer);
  console.log("Documento acortado creado!");
});