$(document).ready(function(){

	//MUTEX

		var LOAD_FIRST_TIME = true;
		GET_LAST_NOTIFY = function(){


		var STATIC_DOMAIN_ = "",
		    URL_HISTORY_ = STATIC_DOMAIN_+"/api/v1/historialventa/?api_key=special-key";
		
		$.ajax({

		url : URL_HISTORY_,
		type : "GET",

		//beforeSend : function(){ synchronized = true; },
		success : function(data){

			console.log(data)


			if ( data.objects.length > 0 ){

				var last_folio = $(".str-activity").children().first().find(".folio_el").html() || "";


				if( LOAD_FIRST_TIME ){
				//si es la primera vez que se carga el sitio etnonces se insertan todas las notificaciones
					activity_admisel.render(data);
					LOAD_FIRST_TIME = false;
					setTimeout( GET_LAST_NOTIFY , 1000)
					return true;

				}

				if( last_folio != data.objects[0].folio && $(".str-activity").html() != "" ){
				//si las nuevas ventas regresadas por AJAX tiene alguna venta no ingresada en el timeline entonces Agrega nueva venta al timeline...
					activity_admisel.append_new_notify_one_by_one ( data.objects) ;


				}

			}else{


				var $node_activity = $(".loader");
				$node_activity.html("<strong>No hay ventas en Admisel  <br> </br> <h1> :( </h1> </strong>"); //.slideUp('slow');


			}


				setTimeout( GET_LAST_NOTIFY , 1000)


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

  /*

		 Summary :  Rendero de todas las notificaciones
  */
  	render : function(data){


		var self = this;

		var $node_activity = $(".str-activity");
		$node_activity.html("");
		$(".loader").hide();

		$.each( data.objects , function(index , activity){

			current_el = self.render_notify(activity);
			$node_activity.append(current_el);

		});

		$("abbr.timeago").timeago();

	},


  /*

		 Summary : Renderea una a una notifiaccion
  */

	append_new_notify_one_by_one : function(notifies){

		var $node_activity = $(".str-activity");

		var last_folio = $(".str-activity").children().first().find(".folio_el").html() || "";
		var self = this;

		$.each( notifies , function(index , notify ){



			if(last_folio ==  notify.folio){
				return false;
			}

			//if(parseInt(last_folio) !=  parseInt(notify.folio)){
			//este elemento no ha sido ingresado
			current_el = self.render_notify(notify);
			$node_activity.prepend( $(current_el).fadeIn('slow') ); //.slideUp('slow');

			//}


		});

		$("abbr.timeago").timeago();
	},




  /*

		 Summary : Regresa el template de la notificacion
  */
  render_notify : function(notify){


		activity = notify;

		return  '<div class="child">'+
			'<div class="sucursal_name"> <span class="actor">'+ activity.sucursal.nombre+'</span><span class="verb"> hizo una venta </span> <abbr class="timeago" title="'+activity.fecha+'"></abbr> </div>'+
			'<div class="activity"> Ha finalizado la venta con el folio : <strong class="folio_el">'+activity.folio+'</strong> </div>'+
			'<div class="activity_report"> Total productos vendidos : <strong> '+activity.total_productos+'</strong> </div>'+
			'<div class="activity_report"> Total : <strong> $'+activity.total+'</strong> </div>'+
			'<div class="activity_report"> venta realizada a: <strong> '+activity.nombre_comprador+'</strong> </div>'+
			'</br>'+
			'<div class="activity_report"> <a  href="https://cdn-ticket.s3.amazonaws.com/'+activity.url_reporte+'" target="_blank"> Click para ver el reporte detallado </a> </div>'+
			'</div>';





  }

  };//end OBJ



});
