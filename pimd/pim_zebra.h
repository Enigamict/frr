/*
 * PIM for Quagga
 * Copyright (C) 2008  Everton da Silva Marques
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; see the file COPYING; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
 */

#ifndef PIM_ZEBRA_H
#define PIM_ZEBRA_H

#include <zebra.h>
#include "zclient.h"

#include "pim_ifchannel.h"

void pim_zebra_init(void);
void pim_zebra_zclient_update(struct vty *vty);

void pim_scan_individual_oil(struct channel_oil *c_oil, int in_vif_index);
void pim_scan_oil(struct pim_instance *pim_matcher);

void pim_forward_start(struct pim_ifchannel *ch);
void pim_forward_stop(struct pim_ifchannel *ch);

void sched_rpf_cache_refresh(struct pim_instance *pim);
struct zclient *pim_zebra_zclient_get(void);

void pim_zebra_update_all_interfaces(struct pim_instance *pim);
void pim_zebra_upstream_rpf_changed(struct pim_instance *pim,
				    struct pim_upstream *up,
				    struct pim_rpf *old);

void pim_zebra_interface_set_master(struct interface *vrf,
				    struct interface *ifp);
#endif /* PIM_ZEBRA_H */
