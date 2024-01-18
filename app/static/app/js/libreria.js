function eliminar(url){

    if(confirm("Estas seguro?")){
        location.href = url
    }
}
/* data table personas */
let dataTable;
let dataTableIsInitialized = false;


const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await listPersonas();

    dataTable = $("#table_personas").DataTable({
        "language":{
            "url":"//cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json"
        }
    });

    dataTableIsInitialized = true;
};
const listPersonas =async()=>{
    try{
        const response = await fetch('http://127.0.0.1:8000/lista_personas/')
        const data = await response.json()
        let content = ` `
        data.personas.forEach((personas)=>{
            content += `
            <tr>
                    <td>${personas.codigo}</td>
                    <td>${personas.nombre}</td>
                    <td>${personas.apellido}</td>
                    <td><a class='btn btn-primary btn-sm' data-bs-toggle="modal" data-bs-target="#crear_socio" ><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/>
                  </svg></a></td>
                </tr>
            `
        });
        personas.innerHTML = content
    }catch(ex){
        console.log(ex);
    }


};

window.addEventListener('load', async () =>{
    await initDataTable();
});



/* datatable socios */ 
let dataTablesocios;
let dataTableIsInitializedsocios = false;


const initDataTablesocios = async () => {
    if (dataTableIsInitializedsocios) {
        dataTablesocios.destroy();
    }

    await listsocios();

    dataTablesocios = $("#table_socios").DataTable({
        "language":{
            "url":"//cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json"
        }
    });

    dataTableIsInitializedsocios = true;
};
const listsocios =async()=>{
    try{
        const response = await fetch('http://127.0.0.1:8000/lista_socios/')
        const data = await response.json()
        let content = ` `
        data.socios.forEach((socios)=>{
            content += `
            <tr>
                    <td>${socios.id}</td>
                    <td>${socios.nombre}</td>
                    <td>${socios.apellido}</td>
                    <td>${socios.cuota}</td>
                    <td>${socios.ciclo}</td>
                    <td>${socios.codigo}</td>
                </tr>
            `
        });
        socios.innerHTML = content
    }catch(ex){
        console.log(ex);
    }


};

window.addEventListener('load', async () =>{
    await initDataTablesocios();
});
