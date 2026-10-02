
import streamlit as st
import random

st.set_page_config(
    page_title="FisioMúsculo IA",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================
# ESTILO
# =========================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #eaf4ff 0%, #f7fbff 55%, #ffffff 100%);
    }
    .block-container {
        max-width: 820px;
        padding-top: 2.2rem;
        padding-bottom: 2rem;
    }
    h1 {
        font-size: 2.1rem !important;
        margin-bottom: 0.2rem !important;
    }
    h2, h3 {
        color: #17324d;
    }
    .subtle {
        color: #486581;
        font-size: 0.95rem;
    }
    .question-card {
        background: rgba(255,255,255,0.92);
        border: 1px solid #d7e6f5;
        border-radius: 18px;
        padding: 1.2rem 1.2rem 1rem 1.2rem;
        box-shadow: 0 5px 18px rgba(40,85,125,.08);
        margin-bottom: 1rem;
    }
    .level-badge {
        display: inline-block;
        padding: 0.2rem 0.65rem;
        border-radius: 999px;
        background: #dceeff;
        color: #174a73;
        font-weight: 700;
        font-size: .88rem;
        margin-bottom: .7rem;
    }
    .score-box {
        background: #ffffff;
        border: 1px solid #d7e6f5;
        border-radius: 14px;
        padding: .9rem 1rem;
        margin-bottom: .8rem;
    }
    div.stButton > button[kind="primary"] {
        width: 100%;
        font-weight: 700;
        border-radius: 12px;
        min-height: 46px;
    }
    div.stButton > button:not([kind="primary"]) {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# BANCO DE PREGUNTAS
# Cada pregunta contiene:
# nivel, pregunta, opciones, correcta, feedback_correcto, feedback_error
# =========================
QUESTIONS = [
# NIVEL 1
{"level":1,"q":"¿Cuál es la función fisiológica principal del tejido muscular?","options":["Producir hormonas","Generar fuerza mecánica","Almacenar calcio extracelular","Transportar oxígeno"],"answer":"Generar fuerza mecánica","ok":"Correcto. El tejido muscular está especializado en generar fuerza mecánica mediante proteínas contráctiles dependientes de ATP y Ca²⁺.","bad":"Revisa la función general del tejido muscular: su rasgo central es la generación de fuerza mecánica."},
{"level":1,"q":"¿Qué proteínas participan directamente en la generación de fuerza muscular?","options":["Actina y miosina","Colágeno y elastina","Troponina y ATPasa","Calsecuestrina y actinina"],"answer":"Actina y miosina","ok":"Correcto. La interacción actina-miosina es la base mecánica de la contracción.","bad":"Piensa en los filamentos contráctiles principales: uno delgado y otro grueso."},
{"level":1,"q":"¿Cuál propiedad muscular corresponde a responder ante un estímulo eléctrico mediante cambios del potencial de membrana?","options":["Elasticidad","Extensibilidad","Excitabilidad","Contractilidad"],"answer":"Excitabilidad","ok":"Correcto. La excitabilidad es la capacidad de responder a un estímulo generando cambios eléctricos de membrana.","bad":"No se refiere a acortarse, sino a responder eléctricamente a un estímulo."},
{"level":1,"q":"La capacidad de generar tensión mediante la interacción actina-miosina corresponde a:","options":["Excitabilidad","Contractilidad","Elasticidad","Extensibilidad"],"answer":"Contractilidad","ok":"Correcto. La contractilidad permite desarrollar tensión y producir acortamiento.","bad":"Busca la propiedad directamente relacionada con producir fuerza o tensión."},
{"level":1,"q":"¿Cuál es la secuencia correcta de organización del músculo esquelético?","options":["Fibra → fascículo → sarcómero → músculo","Fascículo → fibra → miofibrilla → sarcómero","Sarcómero → fascículo → fibra → miofibrilla","Miofibrilla → músculo → fascículo → sarcómero"],"answer":"Fascículo → fibra → miofibrilla → sarcómero","ok":"Correcto. El fascículo contiene fibras; las fibras contienen miofibrillas; las miofibrillas están organizadas en sarcómeros.","bad":"Ordena de una estructura mayor a una menor dentro del músculo."},
{"level":1,"q":"La fibra muscular esquelética se caracteriza por ser:","options":["Fusiforme y mononucleada","Cilíndrica, larga y multinucleada","Ramificada y mononucleada","Esférica y multinucleada"],"answer":"Cilíndrica, larga y multinucleada","ok":"Correcto. Las fibras esqueléticas son largas, cilíndricas y multinucleadas.","bad":"Recuerda la morfología típica de la fibra muscular esquelética."},
{"level":1,"q":"Los núcleos de la fibra muscular esquelética se encuentran principalmente:","options":["En posición central","Dentro del sarcómero","En posición periférica","En los túbulos T"],"answer":"En posición periférica","ok":"Correcto. Los núcleos de la fibra esquelética se ubican en la periferia celular.","bad":"En músculo esquelético los núcleos no se encuentran habitualmente en el centro de la célula."},
{"level":1,"q":"¿Dónde se almacena una elevada concentración de Ca²⁺ intracelular en el músculo esquelético?","options":["Núcleo","Retículo sarcoplásmico","Sarcolema","Miofibrilla"],"answer":"Retículo sarcoplásmico","ok":"Correcto. El retículo sarcoplásmico almacena Ca²⁺ y lo libera durante la excitación-contracción.","bad":"Busca el organelo especializado en almacenar calcio intracelular."},
{"level":1,"q":"Un sarcómero está delimitado por:","options":["Dos líneas M","Dos bandas A","Dos líneas Z","Dos bandas H"],"answer":"Dos líneas Z","ok":"Correcto. El sarcómero se extiende entre dos líneas Z.","bad":"La unidad funcional del músculo estriado está delimitada por dos estructuras iguales en sus extremos."},
{"level":1,"q":"El filamento grueso del sarcómero está formado principalmente por:","options":["Actina","Miosina","Troponina","Tropomiosina"],"answer":"Miosina","ok":"Correcto. La miosina forma el filamento grueso.","bad":"El filamento grueso contiene las cabezas motoras responsables de formar puentes cruzados."},
{"level":1,"q":"El filamento delgado contiene principalmente:","options":["Actina","Miosina II","Calsecuestrina","MLCK"],"answer":"Actina","ok":"Correcto. La actina constituye el componente principal del filamento delgado.","bad":"El filamento delgado es el que expone sitios de unión para la miosina."},
{"level":1,"q":"¿Qué subunidad de la troponina presenta alta afinidad por Ca²⁺?","options":["Troponina T","Troponina I","Troponina C","Troponina M"],"answer":"Troponina C","ok":"Correcto. La troponina C es la subunidad que se une al Ca²⁺.","bad":"La letra de esta subunidad coincide con el ion que regula la contracción."},
{"level":1,"q":"La troponina I cumple principalmente la función de:","options":["Unirse al Ca²⁺","Inhibir la interacción actina-miosina","Hidrolizar ATP","Almacenar Ca²⁺"],"answer":"Inhibir la interacción actina-miosina","ok":"Correcto. La troponina I tiene función inhibitoria sobre la interacción actina-miosina.","bad":"Recuerda que la subunidad I se asocia a una función inhibitoria."},
{"level":1,"q":"¿Qué proteína se encuentra sobre el surco de la hélice de actina?","options":["Miosina","Calsecuestrina","Tropomiosina","Calmodulina"],"answer":"Tropomiosina","ok":"Correcto. La tropomiosina se dispone sobre el surco de la hélice de actina.","bad":"Es una proteína reguladora del filamento delgado."},
{"level":1,"q":"Durante la contracción del sarcómero, las líneas Z:","options":["Se separan","Desaparecen","Se aproximan","Permanecen necesariamente inmóviles"],"answer":"Se aproximan","ok":"Correcto. El sarcómero se acorta porque las líneas Z se acercan.","bad":"Si el sarcómero se acorta, sus extremos deben acercarse."},
{"level":1,"q":"Durante la contracción, ¿qué banda mantiene aproximadamente su ancho?","options":["Banda A","Banda I","Zona H","Línea Z"],"answer":"Banda A","ok":"Correcto. La banda A mantiene su longitud porque corresponde a la longitud del filamento grueso.","bad":"Busca la banda asociada a la longitud del filamento grueso."},
{"level":1,"q":"El mecanismo de contracción muscular se explica mediante el modelo de:","options":["Transporte activo","Filamentos deslizantes","Difusión facilitada","Osmosis celular"],"answer":"Filamentos deslizantes","ok":"Correcto. Los filamentos delgados se deslizan sobre los gruesos sin acortarse ellos mismos.","bad":"La contracción no implica que los filamentos se hagan más cortos."},
{"level":1,"q":"¿Qué ocurre con los filamentos delgados durante el acortamiento muscular?","options":["Se destruyen","Se deslizan sobre los gruesos","Aumentan de longitud","Se convierten en miosina"],"answer":"Se deslizan sobre los gruesos","ok":"Correcto. El deslizamiento de actina sobre miosina acorta el sarcómero.","bad":"Aplica el modelo de filamentos deslizantes."},
{"level":1,"q":"La energía necesaria para el ciclo de los puentes cruzados proviene principalmente de:","options":["Ca²⁺","Na⁺","ATP","Acetilcolina"],"answer":"ATP","ok":"Correcto. El ATP es esencial para el ciclo mecánico de la cabeza de miosina.","bad":"Busca la molécula energética utilizada directamente por la cabeza de miosina."},
{"level":1,"q":"¿Qué proteína puede almacenar grandes cantidades de Ca²⁺ dentro del retículo sarcoplásmico?","options":["Calmodulina","Calsecuestrina","Tropomiosina","Actinina"],"answer":"Calsecuestrina","ok":"Correcto. La calsecuestrina fija Ca²⁺ dentro del retículo sarcoplásmico.","bad":"Es una proteína del retículo sarcoplásmico especializada en fijar calcio."},

# NIVEL 2
{"level":2,"q":"¿Qué evento inicia la secuencia en la unión neuromuscular?","options":["Unión de Ca²⁺ a troponina","Llegada del potencial de acción al terminal axónico","Activación de la bomba de Ca²⁺","Unión de ATP a miosina"],"answer":"Llegada del potencial de acción al terminal axónico","ok":"Correcto. La llegada del potencial de acción al terminal nervioso inicia la transmisión neuromuscular.","bad":"Antes de liberar acetilcolina debe llegar una señal eléctrica al terminal nervioso."},
{"level":2,"q":"La llegada del potencial de acción al terminal nervioso provoca la apertura de:","options":["Canales de Ca²⁺ dependientes de voltaje","Receptores nicotínicos","Canales de rianodina","Bombas de Ca²⁺"],"answer":"Canales de Ca²⁺ dependientes de voltaje","ok":"Correcto. El Ca²⁺ presináptico entra a través de canales dependientes de voltaje.","bad":"El evento presináptico clave es la entrada de Ca²⁺."},
{"level":2,"q":"El aumento de Ca²⁺ en el terminal presináptico provoca:","options":["Degradación de acetilcolina","Exocitosis de vesículas de acetilcolina","Activación de la miosina","Relajación muscular"],"answer":"Exocitosis de vesículas de acetilcolina","ok":"Correcto. El Ca²⁺ presináptico gatilla la exocitosis de ACh.","bad":"Relaciona la entrada de Ca²⁺ presináptico con la liberación del neurotransmisor."},
{"level":2,"q":"La acetilcolina se une en la placa motora a receptores:","options":["Muscarínicos","Metabotrópicos","Nicotínicos","De rianodina"],"answer":"Nicotínicos","ok":"Correcto. La placa motora expresa receptores nicotínicos de acetilcolina.","bad":"En la unión neuromuscular del músculo esquelético el receptor es ionotrópico y nicotínico."},
{"level":2,"q":"Después de la unión de acetilcolina a sus receptores se genera inicialmente:","options":["Potencial de placa terminal","Liberación de Ca²⁺ cardíaco","Fosforilación de miosina","Activación de calmodulina"],"answer":"Potencial de placa terminal","ok":"Correcto. La activación de receptores nicotínicos genera el potencial de placa terminal.","bad":"Piensa en el cambio eléctrico postsináptico inmediato."},
{"level":2,"q":"¿Cuál es una función fundamental de los túbulos T?","options":["Sintetizar ATP","Propagar el potencial de acción al interior de la fibra","Degradar acetilcolina","Producir actina"],"answer":"Propagar el potencial de acción al interior de la fibra","ok":"Correcto. Los túbulos T llevan la despolarización hacia el interior de la fibra.","bad":"Los túbulos T son invaginaciones del sarcolema especializadas en conducción eléctrica."},
{"level":2,"q":"Una tríada muscular está constituida por:","options":["Tres túbulos T","Dos túbulos T y una cisterna","Un túbulo T y dos cisternas terminales","Tres cisternas terminales"],"answer":"Un túbulo T y dos cisternas terminales","ok":"Correcto. La tríada contiene un túbulo T flanqueado por dos cisternas del retículo sarcoplásmico.","bad":"La estructura central es un túbulo T y a cada lado hay una cisterna."},
{"level":2,"q":"Los receptores DHPR funcionan principalmente como:","options":["Enzimas degradadoras de ATP","Sensores de voltaje","Receptores de acetilcolina","Bombas de Ca²⁺"],"answer":"Sensores de voltaje","ok":"Correcto. En el músculo esquelético, DHPR detecta la despolarización de la membrana del túbulo T.","bad":"Su activación depende del cambio de voltaje de la membrana."},
{"level":2,"q":"La activación de DHPR en músculo esquelético estimula:","options":["Receptores RyR1","Receptores nicotínicos","MLCK","Calmodulina"],"answer":"Receptores RyR1","ok":"Correcto. El cambio conformacional de DHPR activa RyR1 en el retículo sarcoplásmico.","bad":"Busca el canal de liberación de Ca²⁺ del retículo sarcoplásmico."},
{"level":2,"q":"¿Cuál es la consecuencia inmediata de la apertura de RyR1?","options":["Entrada de Na⁺ desde el exterior","Liberación de Ca²⁺ desde el retículo sarcoplásmico","Producción de acetilcolina","Captación de Ca²⁺ por el retículo"],"answer":"Liberación de Ca²⁺ desde el retículo sarcoplásmico","ok":"Correcto. RyR1 libera Ca²⁺ almacenado hacia el citosol.","bad":"RyR1 es el canal de salida de calcio del retículo sarcoplásmico."},
{"level":2,"q":"Después de liberarse desde el retículo sarcoplásmico, el Ca²⁺ se une a:","options":["Troponina C","Miosina II","Actina-G","Calsecuestrina"],"answer":"Troponina C","ok":"Correcto. La unión de Ca²⁺ a troponina C inicia el cambio regulador del filamento delgado.","bad":"Es la subunidad reguladora de la troponina que reconoce Ca²⁺."},
{"level":2,"q":"¿Qué ocurre después de la unión de Ca²⁺ a troponina C?","options":["La tropomiosina expone los sitios de unión de la actina","Se cierran los receptores nicotínicos","Se destruye ATP","El Ca²⁺ vuelve inmediatamente al retículo"],"answer":"La tropomiosina expone los sitios de unión de la actina","ok":"Correcto. La tropomiosina se desplaza y deja disponibles los sitios de unión para miosina.","bad":"El efecto regulador del Ca²⁺ ocurre sobre el complejo troponina-tropomiosina."},
{"level":2,"q":"La exposición de los sitios activos de actina permite:","options":["Unión actina-miosina","Activación de acetilcolina","Formación de túbulos T","Síntesis de Ca²⁺"],"answer":"Unión actina-miosina","ok":"Correcto. Al quedar expuestos los sitios, las cabezas de miosina pueden formar puentes cruzados.","bad":"Los sitios activos de actina sirven para unirse a la cabeza de miosina."},
{"level":2,"q":"Cuando una nueva molécula de ATP se une a la cabeza de miosina:","options":["La miosina se separa de la actina","Se libera Ca²⁺ del retículo","Se activa troponina C","Se libera acetilcolina"],"answer":"La miosina se separa de la actina","ok":"Correcto. La unión de ATP reduce la afinidad de miosina por actina y permite su desprendimiento.","bad":"El ATP es necesario para romper el puente cruzado."},
{"level":2,"q":"La hidrólisis de ATP en la cabeza de miosina produce:","options":["ADP + Pi","AMP + Ca²⁺","ATP + Pi","ADP + Na⁺"],"answer":"ADP + Pi","ok":"Correcto. La hidrólisis parcial de ATP deja ADP y Pi asociados a la cabeza de miosina.","bad":"La hidrólisis de ATP genera los productos clásicos ADP y fosfato inorgánico."},
{"level":2,"q":"Mientras el Ca²⁺ citosólico permanezca elevado:","options":["Se mantienen disponibles los sitios de interacción actina-miosina","Se bloquean los sitios de actina","Desaparece la troponina","Se impide el ciclo de puentes cruzados"],"answer":"Se mantienen disponibles los sitios de interacción actina-miosina","ok":"Correcto. El Ca²⁺ mantiene desplazada la tropomiosina y permite continuar los puentes cruzados.","bad":"Mientras el Ca²⁺ siga unido a troponina C, los sitios de actina permanecen accesibles."},
{"level":2,"q":"¿Qué condición favorece la relajación del músculo esquelético?","options":["Elevación persistente de Ca²⁺ citosólico","Disminución del Ca²⁺ citosólico","Aumento de acetilcolina","Apertura persistente de RyR1"],"answer":"Disminución del Ca²⁺ citosólico","ok":"Correcto. La relajación requiere reducir el Ca²⁺ citosólico.","bad":"La contracción se mantiene mientras el Ca²⁺ citosólico está elevado."},
{"level":2,"q":"Durante la relajación, el Ca²⁺ es transportado principalmente:","options":["Desde el retículo sarcoplásmico al citosol","Desde el citosol al retículo sarcoplásmico","Desde el núcleo al sarcolema","Desde la actina a la miosina"],"answer":"Desde el citosol al retículo sarcoplásmico","ok":"Correcto. Las bombas de Ca²⁺ recaptan calcio hacia el retículo sarcoplásmico.","bad":"La relajación necesita retirar Ca²⁺ del citosol."},
{"level":2,"q":"Al disminuir el Ca²⁺ citosólico:","options":["La tropomiosina vuelve a bloquear los sitios de la actina","Se activan más puentes cruzados","Aumenta la unión Ca²⁺-troponina","Se abren continuamente los RyR1"],"answer":"La tropomiosina vuelve a bloquear los sitios de la actina","ok":"Correcto. Al disminuir Ca²⁺, la regulación vuelve al estado de reposo.","bad":"Sin Ca²⁺ unido a troponina C, la tropomiosina recupera su posición inhibitoria."},
{"level":2,"q":"¿Cuál secuencia representa mejor el acoplamiento excitación-contracción esquelético?","options":["PA → DHPR → RyR1 → Ca²⁺ → troponina → puentes cruzados","Ca²⁺ → PA → MLCK → troponina","ATP → acetilcolina → calmodulina → RyR1","RyR1 → acetilcolina → DHPR → Ca²⁺"],"answer":"PA → DHPR → RyR1 → Ca²⁺ → troponina → puentes cruzados","ok":"Correcto. Esa es la secuencia fisiológica central del acoplamiento excitación-contracción esquelético.","bad":"Ordena los eventos desde la despolarización hasta la interacción actina-miosina."},

# NIVEL 3
{"level":3,"q":"El músculo cardíaco se caracteriza por presentar:","options":["Sarcómeros y discos intercalares","Cuerpos densos y ausencia de sarcómeros","Ausencia de actina","Control exclusivamente somático"],"answer":"Sarcómeros y discos intercalares","ok":"Correcto. El músculo cardíaco es estriado y sus células se conectan mediante discos intercalares.","bad":"Recuerda que es un músculo estriado, pero formado por células conectadas entre sí."},
{"level":3,"q":"Las gap junctions del músculo cardíaco se localizan principalmente en:","options":["Túbulos T","Discos intercalares","Sarcómeros","Cisternas terminales"],"answer":"Discos intercalares","ok":"Correcto. Las gap junctions de los discos intercalares facilitan la comunicación eléctrica entre cardiomiocitos.","bad":"Busca la estructura de unión entre células musculares cardíacas."},
{"level":3,"q":"Las uniones comunicantes cardíacas favorecen:","options":["Contracción sincrónica","Contracción voluntaria","Inhibición eléctrica","Destrucción del Ca²⁺"],"answer":"Contracción sincrónica","ok":"Correcto. Las gap junctions permiten propagación eléctrica célula a célula y sincronía contráctil.","bad":"La principal consecuencia de comunicar eléctricamente las células es coordinar su activación."},
{"level":3,"q":"El potencial de acción cardíaco se origina normalmente en células marcapasos del:","options":["Nodo sinoauricular","Retículo sarcoplásmico","Nodo motor","Sarcómero"],"answer":"Nodo sinoauricular","ok":"Correcto. El nodo sinoauricular genera normalmente el ritmo cardíaco.","bad":"Piensa en el marcapasos fisiológico del corazón."},
{"level":3,"q":"Durante el potencial de acción cardíaco, el Ca²⁺ extracelular entra principalmente mediante:","options":["Canales de Ca²⁺ tipo L","Receptores nicotínicos","RyR1 exclusivamente","Bombas de Na⁺"],"answer":"Canales de Ca²⁺ tipo L","ok":"Correcto. Los canales tipo L permiten la entrada de Ca²⁺ durante el potencial de acción cardíaco.","bad":"La entrada de Ca²⁺ extracelular ocurre por canales dependientes de voltaje tipo L."},
{"level":3,"q":"En el músculo cardíaco, el Ca²⁺ que ingresa desde el exterior:","options":["Estimula liberación adicional de Ca²⁺ desde el retículo sarcoplásmico","Bloquea el retículo sarcoplásmico","Inhibe la troponina","Destruye ATP"],"answer":"Estimula liberación adicional de Ca²⁺ desde el retículo sarcoplásmico","ok":"Correcto. El Ca²⁺ entrante desencadena liberación adicional desde el RS.","bad":"En cardiomiocitos, el calcio que entra actúa como señal para liberar más calcio."},
{"level":3,"q":"Este fenómeno cardíaco recibe el nombre de:","options":["Inhibición por Ca²⁺","Liberación de Ca²⁺ estimulada por Ca²⁺","Transporte pasivo de ATP","Despolarización mecánica"],"answer":"Liberación de Ca²⁺ estimulada por Ca²⁺","ok":"Correcto. Es el mecanismo de calcium-induced calcium release descrito para músculo cardíaco.","bad":"El Ca²⁺ que entra desencadena la salida de más Ca²⁺ desde el retículo."},
{"level":3,"q":"¿A qué proteína se une el Ca²⁺ para iniciar la contracción cardíaca?","options":["Calmodulina","Troponina","MLCK","Calsecuestrina exclusivamente"],"answer":"Troponina","ok":"Correcto. Al igual que en músculo esquelético, el Ca²⁺ cardíaco regula la contracción mediante troponina.","bad":"El músculo cardíaco es estriado y utiliza el complejo troponina-tropomiosina."},
{"level":3,"q":"El músculo liso se caracteriza por:","options":["Presentar sarcómeros regulares","No presentar sarcómeros","Ser siempre voluntario","Carecer de actina"],"answer":"No presentar sarcómeros","ok":"Correcto. El músculo liso posee actina y miosina, pero no organizadas en sarcómeros.","bad":"Su ausencia de estriaciones se relaciona con la falta de organización sarcomérica."},
{"level":3,"q":"En el músculo liso, la actina se encuentra anclada principalmente a:","options":["Líneas Z exclusivamente","Cuerpos densos y membrana celular","Discos intercalares","Túbulos T"],"answer":"Cuerpos densos y membrana celular","ok":"Correcto. Los cuerpos densos cumplen una función de anclaje para la actina.","bad":"El músculo liso no posee líneas Z; utiliza otra estructura de anclaje."},
{"level":3,"q":"¿Qué estructura sustituye funcionalmente a las líneas Z en el músculo liso?","options":["Caveolas","Cuerpos densos","Discos intercalares","Cisternas terminales"],"answer":"Cuerpos densos","ok":"Correcto. Los cuerpos densos permiten anclar filamentos y transmitir fuerza.","bad":"Busca la estructura de anclaje de actina propia del músculo liso."},
{"level":3,"q":"Respecto a la troponina, el músculo liso:","options":["Tiene abundante troponina C","No utiliza troponina como regulador principal","Solo presenta troponina I","Solo presenta troponina T"],"answer":"No utiliza troponina como regulador principal","ok":"Correcto. En el músculo liso la regulación depende de calmodulina y MLCK, no de troponina.","bad":"La regulación del músculo liso ocurre sobre la miosina y utiliza calmodulina."},
{"level":3,"q":"¿Qué proteína une Ca²⁺ en el músculo liso?","options":["Troponina C","Calmodulina","Actinina","Calsecuestrina"],"answer":"Calmodulina","ok":"Correcto. El Ca²⁺ se une a calmodulina para iniciar la vía contráctil del músculo liso.","bad":"No es troponina; es una proteína reguladora soluble."},
{"level":3,"q":"El complejo Ca²⁺-calmodulina activa:","options":["MLCK","Troponina I","DHPR esquelético","Acetilcolinesterasa"],"answer":"MLCK","ok":"Correcto. El complejo Ca²⁺-calmodulina activa la cinasa de la cadena ligera de miosina.","bad":"La enzima clave fosforila la cadena ligera de miosina."},
{"level":3,"q":"La MLCK produce:","options":["Fosforilación de la cadena ligera de miosina","Desfosforilación de actina","Bloqueo de los canales de Ca²⁺","Formación de sarcómeros"],"answer":"Fosforilación de la cadena ligera de miosina","ok":"Correcto. Esa fosforilación activa la miosina para interactuar con actina.","bad":"La sigla MLCK corresponde a una cinasa de la cadena ligera de miosina."},
{"level":3,"q":"La fosforilación de la miosina en músculo liso permite:","options":["Interacción con actina","Bloqueo permanente de actina","Degradación de miosina","Formación de líneas Z"],"answer":"Interacción con actina","ok":"Correcto. La miosina fosforilada puede formar puentes cruzados con actina.","bad":"La fosforilación activa funcionalmente la cabeza de miosina."},
{"level":3,"q":"Una diferencia estructural importante del músculo liso es que:","options":["Presenta túbulos T grandes","No presenta túbulos T","Presenta tríadas","Presenta discos intercalares"],"answer":"No presenta túbulos T","ok":"Correcto. El músculo liso carece de túbulos T.","bad":"En músculo liso la membrana forma caveolas en vez de un sistema de túbulos T."},
{"level":3,"q":"Las estructuras asociadas a la entrada de Ca²⁺ en el músculo liso son:","options":["Caveolas","Líneas Z","Discos intercalares","Placas motoras"],"answer":"Caveolas","ok":"Correcto. Las caveolas participan en la organización de canales y señalización de Ca²⁺.","bad":"Son invaginaciones pequeñas de membrana presentes en músculo liso."},
{"level":3,"q":"¿Cuál puede estimular la contracción del músculo liso?","options":["Solo una neurona motora somática","Neurotransmisores, hormonas y estímulos mecánicos","Exclusivamente el nodo SA","Únicamente acetilcolina nicotínica"],"answer":"Neurotransmisores, hormonas y estímulos mecánicos","ok":"Correcto. El músculo liso responde a múltiples tipos de estímulos.","bad":"Su control es diverso y no depende solo del sistema nervioso somático."},
{"level":3,"q":"La relajación del músculo liso se favorece cuando:","options":["Aumenta Ca²⁺ y se activa MLCK","Disminuye Ca²⁺ y cesa la actividad de MLCK","Se forman más puentes cruzados","Se incrementa la fosforilación de miosina"],"answer":"Disminuye Ca²⁺ y cesa la actividad de MLCK","ok":"Correcto. Al bajar Ca²⁺ disminuye la activación de calmodulina y MLCK.","bad":"La vía contráctil depende de Ca²⁺-calmodulina y MLCK; al disminuir, se favorece la relajación."},

# NIVEL 4
{"level":4,"q":"Si se bloquean los canales de Ca²⁺ presinápticos de una neurona motora, ¿qué proceso disminuirá directamente?","options":["Liberación de acetilcolina","Unión Ca²⁺-troponina cardíaca","Activación de MLCK","Formación de cuerpos densos"],"answer":"Liberación de acetilcolina","ok":"Correcto. Sin entrada de Ca²⁺ presináptico disminuye la exocitosis de vesículas con acetilcolina.","bad":"El Ca²⁺ presináptico es necesario para la exocitosis del neurotransmisor."},
{"level":4,"q":"Una alteración que impide la unión de acetilcolina a sus receptores nicotínicos afectará primero:","options":["Generación del potencial de placa terminal","Fosforilación de miosina lisa","Automatismo cardíaco","Formación de cuerpos densos"],"answer":"Generación del potencial de placa terminal","ok":"Correcto. Los receptores nicotínicos generan el potencial de placa terminal en la unión neuromuscular.","bad":"Piensa en el primer evento postsináptico dependiente de ACh."},
{"level":4,"q":"Si un potencial de acción muscular no puede propagarse por los túbulos T, se afectará principalmente:","options":["Activación de DHPR en el interior de la fibra","Síntesis de acetilcolina","Formación de actina","Producción de cuerpos densos"],"answer":"Activación de DHPR en el interior de la fibra","ok":"Correcto. Sin propagación por túbulos T, la despolarización no alcanza adecuadamente los DHPR.","bad":"Los túbulos T llevan la señal eléctrica hasta los sensores de voltaje."},
{"level":4,"q":"Si DHPR no experimenta su cambio conformacional, ¿qué evento se verá reducido posteriormente?","options":["Activación de RyR1","Síntesis de miosina","Liberación de acetilcolina presináptica","Formación de ATP mitocondrial"],"answer":"Activación de RyR1","ok":"Correcto. En músculo esquelético, DHPR activa funcionalmente a RyR1.","bad":"Busca el siguiente elemento de la secuencia DHPR → ... → Ca²⁺."},
{"level":4,"q":"Un bloqueo de RyR1 en músculo esquelético producirá principalmente:","options":["Menor liberación de Ca²⁺ desde el retículo sarcoplásmico","Mayor unión de Ca²⁺ a troponina","Mayor formación de puentes cruzados","Activación directa de MLCK"],"answer":"Menor liberación de Ca²⁺ desde el retículo sarcoplásmico","ok":"Correcto. RyR1 es el canal responsable de liberar Ca²⁺ almacenado en el RS.","bad":"RyR1 se encuentra en el retículo sarcoplásmico y controla la salida de Ca²⁺."},
{"level":4,"q":"Si el Ca²⁺ no puede unirse a la troponina C, ¿qué ocurrirá?","options":["La tropomiosina continuará dificultando la interacción actina-miosina","Se activará MLCK","Se liberará más acetilcolina automáticamente","Se producirán cuerpos densos"],"answer":"La tropomiosina continuará dificultando la interacción actina-miosina","ok":"Correcto. Sin Ca²⁺ en troponina C no ocurre el desplazamiento regulador de la tropomiosina.","bad":"La troponina C controla indirectamente la posición de la tropomiosina."},
{"level":4,"q":"Si la concentración citosólica de Ca²⁺ permanece elevada en una fibra esquelética, es esperable que:","options":["La contracción pueda continuar","La tropomiosina bloquee inmediatamente la actina","Se produzca relajación completa","Desaparezcan los sarcómeros"],"answer":"La contracción pueda continuar","ok":"Correcto. La contracción persiste mientras el Ca²⁺ mantenga disponible la interacción actina-miosina.","bad":"El Ca²⁺ elevado mantiene activa la maquinaria contráctil."},
{"level":4,"q":"Una disminución importante de la recaptación de Ca²⁺ hacia el retículo sarcoplásmico dificultaría principalmente:","options":["Relajación muscular","Liberación de acetilcolina","Potencial de placa terminal","Producción de actina"],"answer":"Relajación muscular","ok":"Correcto. Si el Ca²⁺ permanece elevado en el citosol, la relajación se retrasa.","bad":"La relajación exige retirar Ca²⁺ del citosol."},
{"level":4,"q":"Durante una contracción sarcomérica normal, ¿qué combinación es correcta?","options":["Líneas Z se aproximan y banda A permanece constante","Líneas Z se separan y banda A aumenta","Banda A desaparece y línea Z permanece fija","Filamentos de actina disminuyen de longitud"],"answer":"Líneas Z se aproximan y banda A permanece constante","ok":"Correcto. El sarcómero se acorta por deslizamiento; los filamentos no reducen su longitud.","bad":"Aplica el modelo de filamentos deslizantes: cambian las relaciones espaciales, no la longitud de los filamentos."},
{"level":4,"q":"¿Por qué la hidrólisis de ATP es importante durante los puentes cruzados?","options":["Permite cambios en la cabeza de miosina asociados al ciclo contráctil","Produce directamente acetilcolina","Forma troponina C","Abre directamente receptores nicotínicos"],"answer":"Permite cambios en la cabeza de miosina asociados al ciclo contráctil","ok":"Correcto. El ATP permite el ciclo mecanoquímico de la cabeza de miosina.","bad":"El ATP actúa directamente sobre la cabeza de miosina durante el ciclo de puentes cruzados."},
{"level":4,"q":"Si el Ca²⁺ extracelular disminuyera intensamente, ¿qué tejido de los estudiados dependería especialmente de esa fuente para su contracción?","options":["Músculo cardíaco y músculo liso","Solo músculo esquelético","Ningún músculo","Solo fibra esquelética"],"answer":"Músculo cardíaco y músculo liso","ok":"Correcto. Ambos utilizan Ca²⁺ extracelular como parte importante de su mecanismo de contracción.","bad":"Compara la fuente principal de Ca²⁺ entre músculo esquelético, cardíaco y liso."},
{"level":4,"q":"Una célula muscular con sarcómeros, discos intercalares y gap junctions corresponde a:","options":["Músculo cardíaco","Músculo liso multiunitario","Músculo esquelético","Músculo liso unitario"],"answer":"Músculo cardíaco","ok":"Correcto. Esa combinación estructural es característica del músculo cardíaco.","bad":"Los discos intercalares son una clave distintiva del tejido cardíaco."},
{"level":4,"q":"Una célula sin sarcómeros, sin túbulos T y con caveolas corresponde principalmente a:","options":["Músculo liso","Músculo cardíaco","Músculo esquelético","Fibra motora somática"],"answer":"Músculo liso","ok":"Correcto. El músculo liso carece de sarcómeros y túbulos T y presenta caveolas.","bad":"Las caveolas sustituyen funcionalmente parte del sistema de membrana asociado al Ca²⁺."},
{"level":4,"q":"Una célula utiliza Ca²⁺-calmodulina y MLCK. ¿Qué tipo de tejido corresponde?","options":["Músculo liso","Músculo esquelético","Músculo cardíaco","Nervio motor"],"answer":"Músculo liso","ok":"Correcto. La vía Ca²⁺-calmodulina-MLCK es característica del músculo liso.","bad":"Busca el tipo de músculo que no utiliza troponina como regulador principal."},
{"level":4,"q":"Una fibra muscular utiliza Ca²⁺ unido a troponina y obtiene el Ca²⁺ principalmente desde su retículo sarcoplásmico. Según el material, corresponde a:","options":["Músculo esquelético","Músculo liso","Músculo liso multiunitario","Tejido conjuntivo"],"answer":"Músculo esquelético","ok":"Correcto. En el material, el músculo esquelético utiliza Ca²⁺ del retículo sarcoplásmico y regula la contracción mediante troponina.","bad":"Compara la fuente de Ca²⁺ y la proteína reguladora de cada tipo muscular."},
{"level":4,"q":"¿Cuál comparación entre los tres tipos musculares es correcta según la clase?","options":["Cardíaco y liso son involuntarios; esquelético es voluntario","Los tres son voluntarios","Solo el músculo liso es voluntario","Cardíaco y esquelético son involuntarios"],"answer":"Cardíaco y liso son involuntarios; esquelético es voluntario","ok":"Correcto. El esquelético se asocia a control voluntario, mientras cardíaco y liso son involuntarios.","bad":"Distingue control somático del control autónomo y marcapasos."},
{"level":4,"q":"Respecto de la velocidad de contracción presentada en la clase:","options":["Esquelético > cardíaco > liso","Liso > cardíaco > esquelético","Cardíaco > liso > esquelético","Los tres tienen la misma velocidad"],"answer":"Esquelético > cardíaco > liso","ok":"Correcto. La clase señala que el cardíaco es más lento que el esquelético, pero más rápido que el liso.","bad":"Ordena los tres tipos musculares de mayor a menor velocidad de contracción."},
{"level":4,"q":"Un músculo liso unitario puede contraerse de forma sincronizada principalmente porque presenta:","options":["Uniones comunicantes entre células","Sarcómeros","Placas motoras somáticas","Túbulos T grandes"],"answer":"Uniones comunicantes entre células","ok":"Correcto. Las gap junctions permiten que la actividad eléctrica se propague entre células.","bad":"La sincronía depende de la comunicación eléctrica célula a célula."},
{"level":4,"q":"¿Cuál característica permite un mayor control individual de las células del músculo liso multiunitario?","options":["Mayor aislamiento eléctrico entre células","Mayor número de gap junctions","Presencia de discos intercalares","Presencia de sarcómeros"],"answer":"Mayor aislamiento eléctrico entre células","ok":"Correcto. El músculo liso multiunitario presenta células más independientes eléctricamente.","bad":"Para un control fino, las células deben activarse con mayor independencia unas de otras."},
{"level":4,"q":"Un estudiante concluye: “En músculo esquelético y cardíaco el Ca²⁺ actúa sobre troponina, mientras que en músculo liso actúa sobre calmodulina”. Según los materiales, esta afirmación es:","options":["Correcta","Incorrecta porque los tres utilizan calmodulina","Incorrecta porque los tres utilizan troponina","Incorrecta porque el músculo liso no utiliza Ca²⁺"],"answer":"Correcta","ok":"Correcto. Esa diferencia regulatoria es fundamental entre músculo estriado y músculo liso.","bad":"Compara la proteína reguladora que une Ca²⁺ en músculo estriado versus músculo liso."},
]

# =========================
# FUNCIONES
# =========================
def reset_session():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def shuffled_options(question):
    opts = question["options"][:]
    random.shuffle(opts)
    return opts

def choose_question(level, used_ids):
    candidates = [
        i for i, q in enumerate(QUESTIONS)
        if q["level"] == level and i not in used_ids
    ]
    if not candidates:
        candidates = [i for i, q in enumerate(QUESTIONS) if i not in used_ids]
    if not candidates:
        return None
    return random.choice(candidates)

def init_app():
    defaults = {
        "started": False,
        "current_level": 1,
        "question_number": 0,
        "score": 0,
        "attempts": 0,
        "used_ids": set(),
        "current_id": None,
        "current_options": [],
        "answered": False,
        "feedback": "",
        "last_correct": False,
        "correct_streak": 0,
        "incorrect_streak": 0,
        "history": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def load_next_question():
    if st.session_state.question_number >= 10:
        return
    qid = choose_question(st.session_state.current_level, st.session_state.used_ids)
    if qid is None:
        return
    st.session_state.current_id = qid
    st.session_state.used_ids.add(qid)
    st.session_state.current_options = shuffled_options(QUESTIONS[qid])
    st.session_state.attempts = 0
    st.session_state.answered = False
    st.session_state.feedback = ""
    st.session_state.last_correct = False

def adapt_level(correct):
    level = st.session_state.current_level

    if correct:
        st.session_state.correct_streak += 1
        st.session_state.incorrect_streak = 0
        if st.session_state.correct_streak >= 2 and level < 4:
            st.session_state.current_level += 1
            st.session_state.correct_streak = 0
    else:
        st.session_state.incorrect_streak += 1
        st.session_state.correct_streak = 0
        if st.session_state.incorrect_streak >= 2 and level > 1:
            st.session_state.current_level -= 1
            st.session_state.incorrect_streak = 0

# =========================
# APP
# =========================
init_app()

st.title("FisioMúsculo IA")
st.markdown(
    '<div class="subtle">Aplicación adaptativa de fisiología de la contracción muscular</div>',
    unsafe_allow_html=True
)

st.markdown("")

if not st.session_state.started:
    st.markdown("""
    <div class="question-card">
    <b>¿Cómo funciona?</b><br><br>
    • 10 preguntas por sesión.<br>
    • 2 intentos por pregunta.<br>
    • La dificultad aumenta o disminuye según tu desempeño.<br>
    • Recibirás retroalimentación inmediata.<br>
    • Las preguntas se seleccionan de un banco de 80 ítems.
    </div>
    """, unsafe_allow_html=True)

    if st.button("Comenzar sesión", type="primary"):
        st.session_state.started = True
        load_next_question()
        st.rerun()

else:
    if st.session_state.question_number >= 10:
        st.success("Sesión finalizada")
        st.markdown(
            f"""
            <div class="score-box">
            <b>Puntaje final:</b> {st.session_state.score}/10<br>
            <b>Nivel alcanzado:</b> {st.session_state.current_level}
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.session_state.score >= 8:
            st.info("Muy buen dominio de los mecanismos de contracción muscular.")
        elif st.session_state.score >= 6:
            st.info("Buen desempeño. Conviene reforzar los mecanismos que generaron errores.")
        else:
            st.info("Se recomienda reforzar acoplamiento excitación-contracción, regulación por Ca²⁺ y diferencias entre los tres tipos musculares.")

        if st.button("Iniciar nueva sesión", type="primary"):
            reset_session()

    else:
        if st.session_state.current_id is None:
            load_next_question()

        q = QUESTIONS[st.session_state.current_id]

        st.progress(st.session_state.question_number / 10)
        c1, c2, c3 = st.columns(3)
        c1.metric("Pregunta", f"{st.session_state.question_number + 1}/10")
        c2.metric("Nivel", st.session_state.current_level)
        c3.metric("Puntaje", st.session_state.score)

        st.markdown(
            f"""
            <div class="question-card">
            <div class="level-badge">Nivel {q['level']}</div>
            <div style="font-size:1.1rem; font-weight:700; color:#17324d;">
            {q['q']}
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        choice = st.radio(
            "Selecciona una alternativa:",
            st.session_state.current_options,
            key=f"radio_{st.session_state.question_number}_{st.session_state.current_id}",
            disabled=st.session_state.answered
        )

        if not st.session_state.answered:
            if st.button("Responder", type="primary"):
                st.session_state.attempts += 1

                if choice == q["answer"]:
                    st.session_state.score += 1
                    st.session_state.last_correct = True
                    st.session_state.answered = True
                    st.session_state.feedback = q["ok"]
                    st.session_state.history.append({
                        "question": q["q"],
                        "correct": True,
                        "attempts": st.session_state.attempts,
                        "level": q["level"]
                    })
                    adapt_level(True)
                else:
                    if st.session_state.attempts < 2:
                        st.session_state.feedback = (
                            "Respuesta incorrecta. " + q["bad"] +
                            " Te queda 1 intento."
                        )
                    else:
                        st.session_state.last_correct = False
                        st.session_state.answered = True
                        st.session_state.feedback = (
                            "La respuesta correcta es: "
                            f"**{q['answer']}**. {q['bad']}"
                        )
                        st.session_state.history.append({
                            "question": q["q"],
                            "correct": False,
                            "attempts": st.session_state.attempts,
                            "level": q["level"]
                        })
                        adapt_level(False)
                st.rerun()

        if st.session_state.feedback:
            if st.session_state.answered and st.session_state.last_correct:
                st.success(st.session_state.feedback)
            elif st.session_state.answered:
                st.error(st.session_state.feedback)
            else:
                st.warning(st.session_state.feedback)

        if st.session_state.answered:
            if st.button("Siguiente pregunta", type="primary"):
                st.session_state.question_number += 1
                st.session_state.current_id = None
                if st.session_state.question_number < 10:
                    load_next_question()
                st.rerun()

        st.markdown("---")
        if st.button("Reiniciar sesión"):
            reset_session()

st.markdown("")
st.caption("Desarrollado por Cristian Barahona")
