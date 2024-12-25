/*
 * Timer.c
 *
 *  Created on: 2024��6��19��
 *      Author: Administrator
 */
 /* Optimize Code Most(03) */
#pragma GCC push_options
#pragma GCC optimize ("Os")

#include <stdbool.h>
#include <stdlib.h>
#include "Type_define.h"
#include "Timer.api.h"

typedef struct listpoint
{
	uint8 period; 		
	bool* TimeOutFlag;
	struct listpoint* next;
}listpoint;
void Del_point(listpoint* last, listpoint* this);
static listpoint* head = NULL;


void del_point_by_TimeOutFlag(const bool* flag)
{
	listpoint* p, * q;
	p = head;
	q = head->next;
	while (q != NULL && q->TimeOutFlag != flag)
	{
		p = q;
		q = q->next;
	}
	if (q != NULL)
	{
		Del_point(p, q);
	}
}


void Init_Timer()
{
	head = (listpoint*)malloc(sizeof(listpoint));
	head->next = NULL;
}

void Del_point(listpoint* last, listpoint* this)
{
	last->next = this->next;
	free(this);
}

void Check()
{
	listpoint* p;
	listpoint* q;
	p = head;
	q = head->next;
	while (q != NULL)
	{
		q->period--;
		if (q->period == 0)
		{
			*(q->TimeOutFlag) = true;
			Del_point(p, q);
		}
		p = q;
		q = q->next;

	}
}



void Add_point(listpoint* head, uint8 period, bool* TimeOutFlag)
{
	listpoint* p = head;
	while (p->next != NULL)
	{
		if (p->TimeOutFlag == TimeOutFlag)
		{
			p->period = period;
			break;
		}
		p = p->next;
	}
	if (p->next == NULL)
	{
		listpoint* NewPoint = (listpoint*)malloc(sizeof(listpoint));
		NewPoint->period = period;
		NewPoint->TimeOutFlag = TimeOutFlag;
		NewPoint->next = NULL;
		p->next = NewPoint;
	}
}

void Add_Timer(uint8 period, bool* TimeOutFlag)
{
	Add_point(head, period, TimeOutFlag);

}
#pragma GCC pop_options