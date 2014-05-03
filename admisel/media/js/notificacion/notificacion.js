$(document).ready(function(){

	var STATIC_DOMAIN_ = "",
	    URL_HISTORY_ = STATIC_DOMAIN_+"/api/v1/historialventa/?api_key=special-key";
	
	$.ajax({

	url : URL_HISTORY_,
	type : "GET",

	success : function(data){

		activity_admisel.render(data);

	},
	dataType : "json"

	});

/*

	Summary : Rendereo de la respuesta a HTML en forma de actividad DESC
	param : data - Datos JSON recuperados a traves de AJAX

*/
/***********************************************************************************************/

  activity_admisel = {

  	render : function(data){


		var self = this;

		var $node_activity = $(".str-activity");
		$(".loader").hide();

		$.each( data.objects , function(index , activity){

				var current_el = '<div class="child">'+
					'<div class="sucursal_name"> '+ activity.sucursal.nombre+'</div>'+
					'<div class="activity"> Ha finalizado la venta con el folio : <strong>'+activity.folio+'</strong> </div>'+
					'<div class="activity_report"> Total productos vendidos : <strong> '+activity.total_productos+'</strong> </div>'+
					'<div class="activity_report"> Total : <strong> $'+activity.total+'</strong> </div>'+
					'<div class="activity_report"> venta realizada a: <strong> '+activity.nombre_comprador+'</strong> </div>'+
					'</br>'+
					'<div class="activity_report"> <a href="https://cdn-ticket.s3.amazonaws.com/'+activity.url_reporte+'"> Click para ver el reporte detallado </a> </div>'+
					'</div>';


			console.log(activity);
			$node_activity.append(current_el);

		});

	}

  }



});
