function eliminar(){

    confirm("Estas seguro?")
        
    
}
var dataTablePersonas;
var dataTableSocios;



    function actualizarEstado(elemeto,estado) {
       elemeto.classList.remove('green','red')
       elemeto.classList.add(estado ? 'green' : 'red')
    }

   
    window.onload = actualizarEstado;


function forma(argumento){
document.getElementById('inputArgumento').value= argumento
}

const verificarSiPersonaEsMiembro = (codigo) => {
    const datosSocios = dataTableSocios.rows().data().toArray();
    const esMiembro = datosSocios.some(socio => socio.codigo === codigo);
    return esMiembro;
};

const initDataTablePersonas = async () => {
    
    if ($.fn.DataTable.isDataTable("#contenedor_personas #table_personas")) {
        $("#contenedor_personas #table_personas").DataTable().destroy();
    }
    const response = await fetch('http://127.0.0.1:8000/lista_personas/');
    const data = await response.json();
    
    dataTablePersonas = $("#contenedor_personas #table_personas").DataTable({
        "pageLength": 7,
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.21/i18n/Spanish.json"
        },
        "ajax": {
            "url": 'http://127.0.0.1:8000/lista_personas/',
            "dataSrc": "personas"
        },
        
        "columns": [
            { "data": "codigo" },
            { "data": "nombre" },
            { "data": "apellido" },
            {
                "data": null,
                "render": function (data, type, row, meta) {
                    const esMiembro = verificarSiPersonaEsMiembro(row.codigo);
                    if (esMiembro) {
                        return '  ';
                    } else {
                        return `<a  class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#crear_socio" 
                        data-id="${row.id}" data-natillera="${row.natillera}" data-natille="${row.natille}"
                        data-nombre="${row.nombre}" data-apellido="${row.apellido}" data-codigo="${row.codigo}"
                        data-periodicidad="${row.periodicidad}" data-cuota="${row.cuota}"  onclick="forma('flecha')" >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/>
                        </svg>
                    </a>`;
                    }
                }
            }
        ]
    });
};

const initDataTablesocios = async () => {
    
    if ($.fn.DataTable.isDataTable('#contenedor_socios #table_socio')) {
        $("#contenedor_socios #table_socio").DataTable().destroy();
    }

    dataTableSocios = $('#contenedor_socios #table_socio').DataTable({
        "pageLength": 5,
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.21/i18n/Spanish.json"
        },
        "ajax": {
            "url": 'http://127.0.0.1:8000/lista_socios/',
            "dataSrc": "socios"
        },
        "columns": [
            { "data": "id" },
            { "data": "nombre" },
            { "data": "apellido" },
            { "data": "cuota" },
            { "data": "ciclo" },
            { "data": "codigo" },
            { "data": "activo",
              "render": function (data,type,row){
                const estadoElemento = document.createElement("div");
                estadoElemento.classList.add('circle', 'estado-circle');
                actualizarEstado(estadoElemento,data);
                return estadoElemento.outerHTML; 
              }
        
        },
        { "data": null, 
        "render": function (data,type,row){
            return `<a data-socioid="${row.id}" class="detalle-socio"  ><svg xmlns="http://www.w3.org/2000/svg" class="user"
            width="16" height="16" fill="currentColor" class="bi bi-person" viewBox="0 0 16 16">
            <path
                d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6m2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0m4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4m-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10s-3.516.68-4.168 1.332c-.678.678-.83 1.418-.832 1.664z" />
        </svg></a>`
        }
    
    }
        ]
    });
   
};

window.addEventListener('load', async () => {
    await initDataTablesocios();
    await initDataTablePersonas();
});

$(document).on('click', '#contenedor_personas #table_personas .btn-primary', function() {
    var socioId = $(this).data('id');
    var natillera = $(this).data('natillera');
    var natille = $(this).data('natille');
    var nombre = $(this).data('nombre');
    var apellido = $(this).data('apellido');
    var codigo = $(this).data('codigo');
    var periodicidad = $(this).data('periodicidad');
    var cuota = $(this).data('cuota');
 
    $('#crear_socio input[name="nombre"]').val(nombre);
    $('#crear_socio input[name="apellido"]').val(apellido);
    $('#crear_socio input[name="codigo"]').val(codigo);
    $('#crear_socio input[name="periodicidad"]').val(periodicidad);
    $('#crear_socio input[name="cuota"]').val(cuota);

    $('#crear_socio').modal('show');
});


$(document).on('click', '.detalle-socio', function () {
    var socioId = $(this).data('socioid');
    window.location.href = '/propiedades_socio/' + socioId;
});



$(document).ready( function () {
    $('#miTabla').DataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.21/i18n/Spanish.json"
        }
    });
} );




