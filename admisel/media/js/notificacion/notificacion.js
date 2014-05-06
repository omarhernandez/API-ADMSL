$(document).ready(function(){

	//MUTEX
	var synchronized = false;

	var STACK_NOTIFY = {

		old_data : [],
		new_data : [],
		last_folio_updated : "",
		last_id_updated : "",
	};

	GET_LAST_NOTIFY = function(){


		var STATIC_DOMAIN_ = "",
		    URL_HISTORY_ = STATIC_DOMAIN_+"/api/v1/historialventa/?api_key=special-key";
		
		$.ajax({

		url : URL_HISTORY_,
		type : "GET",

		//beforeSend : function(){ synchronized = true; },
		success : function(data){



			var last_folio = $(".str-activity").children().first().find(".folio_el").html() || "";


				activity_admisel.render(data);

				setTimeout( GET_LAST_NOTIFY , 2000)


		},
		dataType : "json"

		});

	};


	GET_LAST_NOTIFY();


/*

	Summary : Rendereo de la respuesta a HTML en forma de actividad DESC
	param : data - Datos JSON recuperados a traves de AJAX

*/
/***********************************************************************************************/

  activity_admisel = {

  	render : function(data){


		var self = this;

		var $node_activity = $(".str-activity");
		$node_activity.html("");
		$(".loader").hide();

		$.each( data.objects , function(index , activity){

				var current_el = '<div class="child">'+
					'<div class="sucursal_name"> '+ activity.sucursal.nombre+' <abbr class="timeago" title="'+activity.fecha+'"></abbr> </div>'+
					'<div class="activity"> Ha finalizado la venta con el folio : <strong class="folio_el">'+activity.folio+'</strong> </div>'+
					'<div class="activity_report"> Total productos vendidos : <strong> '+activity.total_productos+'</strong> </div>'+
					'<div class="activity_report"> Total : <strong> $'+activity.total+'</strong> </div>'+
					'<div class="activity_report"> venta realizada a: <strong> '+activity.nombre_comprador+'</strong> </div>'+
					'</br>'+
					'<div class="activity_report"> <a href="https://cdn-ticket.s3.amazonaws.com/'+activity.url_reporte+'"> Click para ver el reporte detallado </a> </div>'+
					'</div>';


			$node_activity.append(current_el);

		});

		$("abbr.timeago").timeago();

	}

  }



});
