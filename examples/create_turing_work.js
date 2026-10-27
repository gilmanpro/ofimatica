const { Document, Packer, Paragraph, TextRun, HeadingLevel } = require('docx');
const fs = require('fs');

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Arial", size: 22 }
      }
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 1 }
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun({ text: "Aportes de Alan Turing e Impacto en el Contexto Actual", bold: true })]
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "Alan Mathison Turing (1912-1954)", bold: true }),
          new TextRun(" fue un matematico, logico y criptografo ingles considerado el padre de la computacion moderna. Sus aportes transformaron la tecnologia del siglo XX y sentaron las bases para el mundo digital en que vivimos.")
        ],
        spacing: { after: 120 }
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("Principales Aportes")]
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "1. Maquina de Turing (1936): ", bold: true }),
          new TextRun("Creo el concepto de maquina universal que formalizo la nocion de algoritmo y computabilidad, estableciendo los limites fundamentales de lo que una computadora puede y no puede hacer.")
        ],
        spacing: { after: 80 }
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "2. Criptanalisis de Enigma: ", bold: true }),
          new TextRun("Durante la Segunda Guerra Mundial, Turing lidero el equipo que rompio el codigo Enigma aleman en Bletchley Park, acortando la guerra y salvando incontables vidas. Invento la maquina Bombe para automatizar el proceso.")
        ],
        spacing: { after: 80 }
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "3. Prueba de Turing (1950): ", bold: true }),
          new TextRun("Propuso el famoso test para evaluar la inteligencia artificial, cuestion fundamental en el desarrollo de la IA moderna.")
        ],
        spacing: { after: 80 }
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "4. Biologia Matematica: ", bold: true }),
          new TextRun("Publico trabajos sobre morfogenesis que anticiparon descubrimientos en reacciones quimicas oscilantes.")
        ],
        spacing: { after: 120 }
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("Impacto en el Contexto Actual")]
      }),
      new Paragraph({
        children: [
          new TextRun("Su trabajo es la base de toda computadora moderna. La tesis de Church-Turing valida que cualquier computadora puede simular cualquier otra. Sin Turing, no existirian los smartphones, internet ni la inteligencia artificial. El reconocimiento facial, los chatbots y los sistemas de busqueda son descendientes directos de sus teorias. El premio Turing y su rostro en el billete de 50 libras britanicas testimonian su legado permanente.")
        ],
        spacing: { after: 200 }
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Respuestas a las Preguntas")]
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "1. Como encontrar informacion util en datos aparentemente incomprensibles?", bold: true })
        ],
        spacing: { before: 120 }
      }),
      new Paragraph({
        children: [
          new TextRun("La mineria de datos modernas aplican exactamente los principios que Turing desarrollo: algoritmos que procesan simbolos para extraer informacion significativa. El trabajo de Turing con Enigma demostro que patrones aparentemente aleatorios ocultan estructuras predecibles. En la era actual, algoritmos de machine learning aplican estas mismas tecnicas para descubrir fraude, predecir comportamientos del consumidor y detectar enfermedades.")
        ],
        spacing: { after: 160 }
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "2. Relacion de Turing con la mineria de datos:", bold: true })
        ],
        spacing: { before: 80 }
      }),
      new Paragraph({
        children: [
          new TextRun("Turing establecio que cualquier proceso mecanico computable puede automatizarse. La mineria de datos es precisamente eso: procesos sistematicos para extraer patrones de grandes volumenes de datos. Sus maquinas universales son el modelo teorico detras de cada algoritmo de busqueda, clasificacion y analisis predictivo. Sin su formalizacion de la computabilidad, la mineria de datos automatizada no existiria.")
        ],
        spacing: { after: 160 }
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "3. Estrategias de Turing para identificar patrones en mensajes cifrados:", bold: true })
        ],
        spacing: { before: 80 }
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "Banburismo: ", bold: true }),
          new TextRun("Tecnica estadistica que exploitaba debilidades en los procedimientos de operacion de Enigma. Buscaba patrones en secuencias cifradas comparando probabilidades de configuraciones.")
        ],
        spacing: { after: 60 }
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "Cribas: ", bold: true }),
          new TextRun("Fragmentos de texto plano conocido dentro del cifrado que servian como claves de busqueda.")
        ],
        spacing: { after: 60 }
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "Maquina Bomba: ", bold: true }),
          new TextRun("Automatizo la eliminacion de configuraciones imposibles, reduciendo miles de posibilidades a solo unas pocas correctas mediante deduccion logica sistematica.")
        ],
        spacing: { after: 200 }
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "Referencias consultadas:", bold: true })
        ]
      }),
      new Paragraph({
        children: [
          new TextRun("1. Wikipedia - Alan Turing: https://en.wikipedia.org/wiki/Alan_Turing")
        ]
      }),
      new Paragraph({
        children: [
          new TextRun("2. Britannica - Alan Turing: https://www.britannica.com/biography/Alan-Turing")
        ]
      }),
      new Paragraph({
        children: [
          new TextRun("3. Stanford Encyclopedia of Philosophy - Alan Turing: https://plato.stanford.edu/entries/turing/")
        ]
      }),
      new Paragraph({
        children: [
          new TextRun("4. Imperial War Museums: https://www.iwm.org.uk/history/second-world-war/how-alan-turing-cracked-the-enigma-code")
        ]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("Trabajo_Alan_Turing.docx", buffer);
  console.log("Documento creado exitosamente.");
});