if(!Sendinel) { var Sendinel = {}; }

Sendinel.Utils = {
    confirmForm : function(form, title) {
        $("#confirmation").dialog({
            modal: true,
            resizable: false,
            draggable: false,
            title: title,
            buttons: {
                "Cancel" : function() {
                    $(this).dialog("close");
                },
                "OK" : function() {
                    form.submit();
                }
            }
        });
        
        if(!$("#confirmation").dialog("isOpen")) {
            $("#confirmation").dialog("open");
        }
    },
    
    goto_url : function(url) {
        if(url) {
            window.location.assign(url);
        }
    },
    
    graft: function(namespace, parent, t, doc) {

        doc = (doc || (parent && parent.ownerDocument) || document);

        var e;

        if(t === undefined) {
            echo( "Can't graft an undefined value");
        } else if(t.constructor == String) {
            e = doc.createTextNode( t );
        } else {

            for(var i = 0; i < t.length; i++) {
                if( i === 0 && t[i].constructor == String ) {
                    var snared = t[i].match( /^([a-z][a-z0-9]*)\.([^\s\.]+)$/i );

                    if( snared ) {
                        e = doc.createElementNS(namespace, snared[1]);
                        e.setAttributeNS(null, 'class', snared[2] );
                        continue;
                    }

                snared = t[i].match( /^([a-z][a-z0-9]*)$/i );

                if( snared ) {
                    e = doc.createElementNS(namespace, snared[1]); // but no class
                    continue;
                }

                // Otherwise:
                e = doc.createElementNS(namespace, "span");
                e.setAttribute(null, "class", "namelessFromLOL" );
                }

                if( t[i] === undefined ) {
                    echo("Can't graft an undefined value in a list!");
                } else if( t[i].constructor == String || t[i].constructor == Array) {
                    this.graft(namespace, e, t[i], doc );
                } else if( t[i].constructor == Number ) {
                    this.graft(namespace, e, t[i].toString(), doc );
                } else if( t[i].constructor == Object ) {
                    // hash's properties => element's attributes
                    for(var k in t[i]) { e.setAttributeNS(null, k, t[i][k] ); }
                } else if( t[i].constructor == Boolean ) {
                    this.graft(namespace, e, t[i] ? 'true' : 'false', doc );
                } else
                    throw "Object " + t[i] + " is inscrutable as an graft arglet.";
            }
        }

        if(parent) parent.appendChild(e);

        return Element.extend(e); // return the topmost created node
    }
};