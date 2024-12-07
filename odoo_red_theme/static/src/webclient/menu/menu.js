/** @odoo-module */

import {Component, useRef, onMounted, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

const ICON = '/openerphk_theme/static/src/img/icon.png'
const animationSpeed = 300;

export class Menu extends Component {
    static template = 'openerphk.Menu'
    static props = ['*']

    setup() {
        this.menuService = useService("menu");
        this.menu = useRef('menu');
        this.currentMenu = useState({id: this.env.services.router.current.hash.menu_id});
        onMounted(()=>{
            this.openMenu();
        })
    }

    openMenu(){
        if (!this.currentMenu.id)return;
        const $menu = $(this.menu.el);
        const $this = $menu.find('[menuID=' + this.currentMenu.id + ']');
        $this.parents('ul').not('.menu').addClass('menu-open').slideDown(animationSpeed).parent("li").addClass('active');

        // 滚动到可视区域
        $this[0].scrollIntoView({
            behavior: 'smooth',
            block: 'center',
        })
    }

    clickMenu(ev, menuID=null) {
        if (menuID){
            this.currentMenu.id = menuID;
        }
        const $menu = $(this.menu.el);
        if ($menu.is('.o_fold')) {
            $menu.removeClass('o_fold');
        }

        const $this = $(ev.target).is('a') ? $(ev.target) : $(ev.target).parent();
        const checkElement = $this.next();

        if (checkElement.is('.children-menu') && checkElement.is(':visible')) {
            checkElement.slideUp(animationSpeed, function () {
                checkElement.removeClass('menu-open');
            });
            checkElement.parent("li").removeClass("active");
        }

        //If the menu is not visible
        else if ((checkElement.is('.children-menu')) && (!checkElement.is(':visible'))) {
            //Get the parent menu
            const parent = $this.parents('ul').first();
            //Close all open menus within the parent
            const ul = parent.find('ul:visible').slideUp(animationSpeed);
            //Remove the menu-open class from the parent
            ul.removeClass('menu-open');
            //Get the parent li
            const parent_li = $this.parent("li");

            //Open the target menu and add the menu-open class
            checkElement.slideDown(animationSpeed, function () {
                //Add the class active to the parent li
                checkElement.addClass('menu-open');
                parent.find('li.active').removeClass('active');
                parent_li.addClass('active');
            });
        }
        //if this isn't a link, prevent the page from being redirected
        if (checkElement.is('.children-menu')) {
            ev.preventDefault();
        }
    }

    foldMenu() {
        const $this = $(this.menu.el);
        const openMenu = this.openMenu.bind(this);
        const promise = $this.find('ul').not('.menu').slideUp(animationSpeed).promise();
        $.when.apply($, [promise]).then(function() {
            $this.toggleClass('o_fold');
            if (!$this.hasClass('o_fold')){
                setTimeout(openMenu, 200);
            }
        });

        $this.find('li.active').removeClass('active');
    }

    getMenuIconData(menu) {
        if (menu.webIconData) {
            return 'data:image/png;base64,' + menu.webIconData;
        } else {
            return ICON;
        }
    }

    getNavIconData() {
        const root = this.menuService.getMenu('root');
        return root.nav_logo ? 'data:image/png;base64,' + root.nav_logo : '/openerphk_theme/static/src/img/icon.png'
    }
}
